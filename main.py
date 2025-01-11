import flet as ft
import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    print("Aviso: Locale 'pt_BR.UTF-8' não encontrado. Usando locale padrão.")
    locale.setlocale(locale.LC_ALL, '')

def calcular_investimento(capital_inicial, aporte_mensal, taxa_juros, periodo):
    """Calcula o montante final de um investimento usando juros compostos."""
    capital_inicial = float(capital_inicial)
    aporte_mensal = float(aporte_mensal)
    taxa_juros = float(taxa_juros) / 100
    periodo = int(periodo)

    montante = capital_inicial
    historico = [montante]

    for _ in range(periodo):
        montante += aporte_mensal
        montante *= (1 + taxa_juros)
        historico.append(montante)

    return historico[1:]  # Ignora o "mês 0"


def main(page: ft.Page):
    page.title = "Simulador de Investimentos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Título
    container_titulo = ft.Container(
        padding=30,
        content=ft.Text(
            "Simulador de Investimentos",
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
    )

    espaco = ft.Container(padding=20)

    # Campos de entrada
    valor_capital_inicial = ft.TextField(
        label="Capital Inicial (R$)", value="1000", text_align=ft.TextAlign.CENTER)
    valor_aporte_mensal = ft.TextField(
        label="Aporte Mensal (R$)", value="200", text_align=ft.TextAlign.CENTER)
    valor_taxa_juros = ft.TextField(
        label="Taxa de Juros Mensal (%)", value="0.5", text_align=ft.TextAlign.CENTER)
    valor_periodo = ft.TextField(
        label="Período (meses)", value="12", text_align=ft.TextAlign.CENTER)

    # ListView para exibir o resultado
    lv = ft.ListView(spacing=10, padding=20, auto_scroll=True, height=400)

    # Função para atualizar o resultado
    def atualizar_resultado(e):
        try:
            historico = calcular_investimento(
                valor_capital_inicial.value,
                valor_aporte_mensal.value,
                valor_taxa_juros.value,
                valor_periodo.value
            )
            lv.controls.clear()

            # Exibir do mês 1 ao mês N
            for i, valor in enumerate(historico, start=1):
                lv.controls.append(ft.Text(
                    f"Mês {i}: {locale.currency(valor, grouping=True)}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ))

            lv.update()
        except ValueError:
            lv.controls.clear()
            lv.controls.append(ft.Text(
                "Por favor, insira valores numéricos válidos!",
                color="red",
                size=16,
                weight=ft.FontWeight.BOLD
            ))
            lv.update()

    # Botão de cálculo
    calcular_btn = ft.ElevatedButton("Calcular", on_click=atualizar_resultado)

    # Layout principal
    page.add(
        ft.SafeArea(
            ft.Container(
                ft.Column(
                    [
                        container_titulo,
                        espaco,
                        valor_capital_inicial,
                        valor_aporte_mensal,
                        valor_taxa_juros,
                        valor_periodo,
                        calcular_btn,
                        lv,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )

ft.app(target=main, port=8080)