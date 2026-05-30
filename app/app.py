from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


APP_TITLE = "SpaceData Monitor"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "space_environmental_risk.csv"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["data"] = pd.to_datetime(df["periodo"] + "-01")
    df["nivel_risco"] = df["nivel_risco"].astype(str)
    return df


def format_number(value: float, suffix: str = "") -> str:
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M{suffix}"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}k{suffix}"
    return f"{value:,.0f}{suffix}".replace(",", ".")


def risk_summary(score: float) -> str:
    if score >= 65:
        return "🚨 Risco crítico: priorizar análise operacional e plano de resposta."
    if score >= 45:
        return "⚠️ Risco alto: acompanhar tendências e preparar ações preventivas."
    if score >= 25:
        return "🟡 Risco moderado: manter monitoramento e validar regiões sensíveis."
    return "🟢 Risco baixo: cenário dentro do comportamento esperado."


def render_header() -> None:
    st.markdown(
        """
        <style>
            .hero {
                padding: 1.4rem 1.6rem;
                border-radius: 1.2rem;
                background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 54%, #0369a1 100%);
                color: white;
                margin-bottom: 1rem;
            }
            .hero h1 {
                margin: 0;
                font-size: 2.2rem;
            }
            .hero p {
                margin: .35rem 0 0 0;
                font-size: 1rem;
                opacity: .95;
            }
            .small-note {
                color: #64748b;
                font-size: .88rem;
            }
            div[data-testid="stMetricValue"] {
                font-size: 1.65rem;
            }
        </style>
        <div class="hero">
            <h1>🛰️ SpaceData Monitor</h1>
            <p>Dashboard de Data Science para monitoramento ambiental com dados inspirados em fontes espaciais e climáticas.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(df: pd.DataFrame) -> tuple[list[str], list[str], tuple]:
    st.sidebar.title("Filtros")
    st.sidebar.caption("Use os filtros para explorar regiões, estados e períodos.")

    regioes = sorted(df["regiao"].unique())
    selected_regions = st.sidebar.multiselect("Regiões", regioes, default=regioes)

    states_options = sorted(df[df["regiao"].isin(selected_regions)]["estado"].unique())
    selected_states = st.sidebar.multiselect("Estados", states_options, default=states_options)

    min_date = df["data"].min().date()
    max_date = df["data"].max().date()
    selected_dates = st.sidebar.slider(
        "Período",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MM/YYYY",
    )

    return selected_regions, selected_states, selected_dates


def apply_filters(df: pd.DataFrame, regions: list[str], states: list[str], dates: tuple) -> pd.DataFrame:
    start_date = pd.to_datetime(dates[0])
    end_date = pd.to_datetime(dates[1])
    return df[
        (df["regiao"].isin(regions))
        & (df["estado"].isin(states))
        & (df["data"].between(start_date, end_date))
    ].copy()


def render_kpis(filtered: pd.DataFrame) -> None:
    col1, col2, col3, col4 = st.columns(4)

    total_fires = filtered["focos_queimada"].sum()
    total_deforestation = filtered["area_desmatada_km2"].sum()
    avg_temp = filtered["temperatura_media_c"].mean()
    avg_risk = filtered["risco_ambiental_score"].mean()

    col1.metric("Focos de queimadas", format_number(total_fires))
    col2.metric("Área desmatada estimada", f"{total_deforestation:,.0f} km²".replace(",", "."))
    col3.metric("Temperatura média", f"{avg_temp:.1f} °C")
    col4.metric("Score médio de risco", f"{avg_risk:.1f}/100")

    st.caption(risk_summary(avg_risk))


def render_overview(filtered: pd.DataFrame) -> None:
    st.subheader("Visão geral")

    trend = (
        filtered.groupby("data", as_index=False)
        .agg(
            focos_queimada=("focos_queimada", "sum"),
            area_desmatada_km2=("area_desmatada_km2", "sum"),
            risco_ambiental_score=("risco_ambiental_score", "mean"),
        )
        .sort_values("data")
    )

    fig_trend = px.line(
        trend,
        x="data",
        y=["focos_queimada", "risco_ambiental_score"],
        markers=True,
        title="Evolução mensal: focos de queimadas e score de risco",
        labels={
            "data": "Período",
            "value": "Valor",
            "variable": "Indicador",
        },
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    left, right = st.columns(2)

    by_state = (
        filtered.groupby(["uf", "estado", "regiao"], as_index=False)
        .agg(
            focos_queimada=("focos_queimada", "sum"),
            area_desmatada_km2=("area_desmatada_km2", "sum"),
            risco_ambiental_score=("risco_ambiental_score", "mean"),
        )
        .sort_values("risco_ambiental_score", ascending=False)
        .head(12)
    )

    fig_bar = px.bar(
        by_state,
        x="estado",
        y="risco_ambiental_score",
        color="regiao",
        title="Top 12 estados por risco ambiental médio",
        labels={"estado": "Estado", "risco_ambiental_score": "Score médio"},
    )
    left.plotly_chart(fig_bar, use_container_width=True)

    fig_scatter = px.scatter(
        filtered,
        x="precipitacao_mm",
        y="temperatura_media_c",
        size="focos_queimada",
        color="nivel_risco",
        hover_name="estado",
        title="Relação entre chuva, temperatura e queimadas",
        labels={
            "precipitacao_mm": "Precipitação (mm)",
            "temperatura_media_c": "Temperatura média (°C)",
            "nivel_risco": "Nível de risco",
        },
    )
    right.plotly_chart(fig_scatter, use_container_width=True)


def render_map(filtered: pd.DataFrame) -> None:
    st.subheader("Mapa de risco ambiental")

    map_df = (
        filtered.groupby(["uf", "estado", "regiao"], as_index=False)
        .agg(
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            focos_queimada=("focos_queimada", "sum"),
            area_desmatada_km2=("area_desmatada_km2", "sum"),
            risco_ambiental_score=("risco_ambiental_score", "mean"),
        )
    )

    fig_map = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        size="focos_queimada",
        color="risco_ambiental_score",
        hover_name="estado",
        hover_data={
            "regiao": True,
            "focos_queimada": ":,",
            "area_desmatada_km2": ":.1f",
            "risco_ambiental_score": ":.1f",
            "latitude": False,
            "longitude": False,
        },
        zoom=3.1,
        height=620,
        mapbox_style="open-street-map",
        title="Distribuição geográfica do risco ambiental",
        labels={"risco_ambiental_score": "Score de risco"},
    )

    fig_map.update_layout(margin={"r": 0, "t": 45, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown(
        """
        <p class="small-note">
        Observação: as coordenadas representam pontos aproximados por estado. O objetivo é criar uma visualização didática
        para publicação via pipeline, não um produto geoespacial de precisão.
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_alerts(filtered: pd.DataFrame) -> None:
    st.subheader("Alertas e priorização")

    alerts = (
        filtered.groupby(["uf", "estado", "regiao"], as_index=False)
        .agg(
            focos_queimada=("focos_queimada", "sum"),
            area_desmatada_km2=("area_desmatada_km2", "sum"),
            precipitacao_mm=("precipitacao_mm", "mean"),
            temperatura_media_c=("temperatura_media_c", "mean"),
            indice_vegetacao_ndvi=("indice_vegetacao_ndvi", "mean"),
            risco_ambiental_score=("risco_ambiental_score", "mean"),
        )
        .sort_values("risco_ambiental_score", ascending=False)
    )

    def classify(score: float) -> str:
        if score >= 65:
            return "Crítico"
        if score >= 45:
            return "Alto"
        if score >= 25:
            return "Moderado"
        return "Baixo"

    alerts["prioridade"] = alerts["risco_ambiental_score"].apply(classify)
    alerts["recomendacao"] = alerts["prioridade"].map(
        {
            "Crítico": "Acionar plano de resposta e investigar causas locais.",
            "Alto": "Criar ação preventiva e acompanhar diariamente.",
            "Moderado": "Monitorar indicadores e comparar com histórico.",
            "Baixo": "Manter acompanhamento periódico.",
        }
    )

    st.dataframe(
        alerts,
        use_container_width=True,
        hide_index=True,
        column_config={
            "risco_ambiental_score": st.column_config.ProgressColumn(
                "Score de risco",
                min_value=0,
                max_value=100,
                format="%.1f",
            ),
            "area_desmatada_km2": st.column_config.NumberColumn("Área desmatada km²", format="%.1f"),
            "precipitacao_mm": st.column_config.NumberColumn("Chuva média mm", format="%.1f"),
            "temperatura_media_c": st.column_config.NumberColumn("Temp. média °C", format="%.1f"),
            "indice_vegetacao_ndvi": st.column_config.NumberColumn("NDVI médio", format="%.3f"),
        },
    )


def render_methodology(df: pd.DataFrame) -> None:
    st.subheader("Metodologia didática")

    st.markdown(
        """
        Esta aplicação foi criada para uma atividade acadêmica de **Data Science + Cloud + DevOps**.

        O dataset é sintético, mas foi estruturado para simular indicadores utilizados em análises ambientais:

        - focos de queimadas;
        - área desmatada estimada;
        - precipitação;
        - temperatura média;
        - índice de vegetação NDVI;
        - score de risco ambiental.

        O **score de risco ambiental** combina os indicadores em uma escala de 0 a 100.
        Valores maiores indicam maior prioridade de análise e resposta.

        O objetivo da turma não é alterar a aplicação. O desafio é criar a pipeline para empacotar este dashboard em Docker,
        publicar a imagem em um Azure Container Registry e fazer o deploy em Azure Container Instance.
        """
    )

    st.code(
        """
Fluxo esperado da pipeline:

Azure DevOps
  → Docker build
  → Azure Container Registry
  → Azure Container Instance
  → URL pública do dashboard
        """.strip(),
        language="text",
    )

    with st.expander("Amostra do dataset"):
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)


def main() -> None:
    df = load_data()
    render_header()

    regions, states, dates = render_sidebar(df)
    filtered = apply_filters(df, regions, states, dates)

    if filtered.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    render_kpis(filtered)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Visão geral", "🗺️ Mapa", "🚨 Alertas", "🧪 Metodologia"]
    )

    with tab1:
        render_overview(filtered)

    with tab2:
        render_map(filtered)

    with tab3:
        render_alerts(filtered)

    with tab4:
        render_methodology(df)


if __name__ == "__main__":
    main()
