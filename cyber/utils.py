import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


SEVERITY_COLORS = {
    "Critical": "#ff3b5c",
    "High":     "#ff8c00",
    "Medium":   "#ffc800",
    "Low":      "#00ff88",
}

STATUS_COLORS = {
    "Open":        "#ff3b5c",
    "In Progress": "#ff8c00",
    "Resolved":    "#00ff88",
}


def risk_gauge(df):
    weights = {"Critical": 10, "High": 7, "Medium": 4, "Low": 1}
    total_weight = sum(weights.values()) * len(df)
    raw = sum(weights.get(s, 0) for s in df["Severity"]) / total_weight * 100 if len(df) else 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(raw, 1),
        number={"suffix": " / 100", "font": {"size": 28, "color": "#e2e8f0"}},
        title={"text": "Overall Risk Score", "font": {"size": 14, "color": "#94a3b8"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#475569"},
            "bar": {"color": "#00d4ff", "thickness": 0.25},
            "bgcolor": "#0d1f3c",
            "bordercolor": "#0d1f3c",
            "steps": [
                {"range": [0,  33], "color": "rgba(0,255,136,0.15)"},
                {"range": [33, 67], "color": "rgba(255,200,0,0.15)"},
                {"range": [67,100], "color": "rgba(255,59,92,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#ff3b5c", "width": 3},
                "thickness": 0.75,
                "value": raw
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(t=40, b=10, l=20, r=20),
    )
    return fig


def severity_bar(df):
    counts = df["Severity"].value_counts().reindex(["Critical", "High", "Medium", "Low"], fill_value=0)
    fig = go.Figure(go.Bar(
        x=counts.index,
        y=counts.values,
        marker_color=[SEVERITY_COLORS[s] for s in counts.index],
        text=counts.values,
        textposition="outside",
        textfont=dict(color="#e2e8f0"),
    ))
    fig.update_layout(
        title="Vulnerabilities by Severity",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        height=280,
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
    )
    return fig


def status_pie(df):
    counts = df["Status"].value_counts()
    fig = go.Figure(go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.5,
        marker=dict(colors=[STATUS_COLORS.get(s, "#94a3b8") for s in counts.index]),
        textfont=dict(color="#e2e8f0"),
    ))
    fig.update_layout(
        title="Vulnerability Status",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        height=280,
        margin=dict(t=40, b=10, l=10, r=10),
        legend=dict(font=dict(color="#94a3b8")),
    )
    return fig


def cvss_radar(df):
    top8 = df.nlargest(8, "CVSS Score")
    fig = go.Figure(go.Scatterpolar(
        r=top8["CVSS Score"].tolist() + [top8["CVSS Score"].iloc[0]],
        theta=top8["Name"].str[:25].tolist() + [top8["Name"].str[:25].iloc[0]],
        fill="toself",
        fillcolor="rgba(0,212,255,0.15)",
        line=dict(color="#00d4ff", width=2),
        name="CVSS"
    ))
    fig.update_layout(
        title="CVSS Score Radar",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10], color="#475569"),
            angularaxis=dict(color="#475569"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=10),
        height=310,
        margin=dict(t=50, b=20, l=20, r=20),
    )
    return fig


def category_bar(df):
    counts = df["Category"].value_counts()
    fig = go.Figure(go.Bar(
        x=counts.values,
        y=counts.index,
        orientation="h",
        marker_color="#7c3aed",
        text=counts.values,
        textposition="outside",
        textfont=dict(color="#e2e8f0"),
    ))
    fig.update_layout(
        title="Vulnerabilities by Category",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        height=280,
        margin=dict(t=40, b=20, l=10, r=30),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(showgrid=False),
    )
    return fig