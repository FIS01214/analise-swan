"""Adaptador mínimo para desenhar os gráficos didáticos com PyROOT.

As funções expostas imitam somente a pequena parte da API de Matplotlib usada
pelos notebooks. Os objetos reais criados são TCanvas, TH1D, TH2D e TGraph.
"""

from __future__ import annotations

from array import array
from pathlib import Path

import numpy as np
import ROOT
from IPython.display import display

# O SWAN e o Colab exibem o TCanvas por JSROOT diretamente no notebook.
ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0)

_CORES = {
    "tab:blue": ROOT.kBlue + 1,
    "tab:orange": ROOT.kOrange + 7,
    "black": ROOT.kBlack,
    "tab:green": ROOT.kGreen + 2,
}


def _cor(valor):
    return _CORES.get(valor, ROOT.kBlack)


class RootAxis:
    def __init__(self, pad, indice):
        self.pad = pad
        self.indice = indice
        self.objetos = []
        self.legend_obj = None

    def _desenhar(self, objeto, opcao=""):
        self.pad.cd()
        objeto.Draw(opcao)
        self.objetos.append(objeto)
        return objeto

    def hist(self, valores, bins=40, range=None, weights=None, histtype="step",
             color="black", label=None, linewidth=1.5, **_):
        valores = np.asarray(valores, dtype=float)
        pesos = None if weights is None else np.asarray(weights, dtype=float)
        contagens, bordas = np.histogram(valores, bins=bins, range=range, weights=pesos)
        hist = ROOT.TH1D(f"h{self.indice}_{len(self.objetos)}", "", len(bordas) - 1,
                         array("d", bordas))
        for i, valor in enumerate(contagens, start=1):
            hist.SetBinContent(i, float(valor))
        hist.SetLineColor(_cor(color))
        hist.SetLineWidth(max(1, int(linewidth)))
        hist.SetFillColor(_cor(color) if histtype != "step" else 0)
        if histtype == "step":
            hist.SetFillStyle(0)
        if label:
            hist.SetTitle(label)
        self._desenhar(hist, "HIST SAME" if self.objetos else "HIST")
        return contagens, bordas, hist

    def stairs(self, valores, bordas, color="black", label=None, linewidth=1.5,
               fill=False, alpha=1.0, **_):
        hist = ROOT.TH1D(f"h{self.indice}_{len(self.objetos)}", "",
                         len(bordas) - 1, array("d", np.asarray(bordas, dtype=float)))
        for i, valor in enumerate(np.asarray(valores, dtype=float), start=1):
            hist.SetBinContent(i, float(valor))
        hist.SetLineColor(_cor(color))
        hist.SetLineWidth(max(1, int(linewidth)))
        hist.SetFillColorAlpha(_cor(color), float(alpha)) if fill else hist.SetFillStyle(0)
        if label:
            hist.SetTitle(label)
        self._desenhar(hist, "HIST SAME" if self.objetos else "HIST")
        return hist

    def errorbar(self, x, y, yerr=None, color="black", ecolor=None, label=None,
                 fmt="none", alpha=0.35, linewidth=1.0, **_):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        ey = np.zeros_like(y) if yerr is None else np.asarray(yerr, dtype=float)
        cor = _cor(ecolor or color)
        banda = ROOT.TGraphAsymmErrors(len(x))
        for indice, (x_valor, y_valor, erro) in enumerate(zip(x, y, ey)):
            banda.SetPoint(indice, float(x_valor), float(y_valor))
            banda.SetPointError(indice, 0.0, 0.0, float(erro), float(erro))
        banda.SetFillColor(cor)
        banda.SetFillStyle(3345)
        banda.SetLineColor(cor)
        banda.SetLineWidth(max(1, int(linewidth)))
        banda.SetTitle("")
        self._desenhar(banda, "3" if not self.objetos else "3 SAME")
        if fmt and fmt != "none" and "-" in str(fmt):
            linha = ROOT.TGraph(len(x), array("d", x), array("d", y))
            linha.SetLineColor(cor)
            linha.SetLineWidth(max(1, int(linewidth)))
            if label:
                linha.SetTitle(str(label))
            self._desenhar(linha, "L SAME")
        return banda

    def hist2d(self, x, y, bins=40, range=None, cmap=None, **_):
        (xmin, xmax), (ymin, ymax) = range
        nx, ny = (bins, bins) if isinstance(bins, int) else bins
        hist = ROOT.TH2D(f"h2_{self.indice}_{len(self.objetos)}", "", nx, xmin, xmax, ny, ymin, ymax)
        # Reserve space for the Z-axis title and color scale on 2D plots.
        self.pad.SetRightMargin(0.20)
        for xv, yv in zip(np.asarray(x, dtype=float), np.asarray(y, dtype=float)):
            hist.Fill(float(xv), float(yv))
        self._desenhar(hist, "COLZ")
        return None, None, None, hist

    def plot(self, x, y, color="black", label=None, linewidth=1.5, **_):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        graph = ROOT.TGraph(len(x), array("d", x), array("d", y))
        graph.SetLineColor(_cor(color))
        graph.SetLineWidth(max(1, int(linewidth)))
        if label:
            graph.SetTitle(label)
        self._desenhar(graph, "AL" if not self.objetos else "L SAME")
        return graph

    def set_xlabel(self, texto):
        self.pad.SetBottomMargin(0.15)
        self._xlabel = str(texto)
        if self.objetos and hasattr(self.objetos[0], "GetXaxis"):
            eixo_x = self.objetos[0].GetXaxis()
            eixo_x.SetTitle(self._xlabel)
            eixo_x.SetTitleSize(0.05)
            eixo_x.SetLabelSize(0.04)

    def set_ylabel(self, texto):
        self.pad.SetLeftMargin(0.18)
        self._ylabel = str(texto)
        if self.objetos and hasattr(self.objetos[0], "GetYaxis"):
            eixo_y = self.objetos[0].GetYaxis()
            eixo_y.SetTitle(self._ylabel)
            eixo_y.SetTitleSize(0.05)
            eixo_y.SetLabelSize(0.04)

    def set_title(self, texto):
        self.pad.SetTitle(str(texto))

    def set_ylim(self, ymin, ymax):
        """Aplicar explicitamente o intervalo Y ao primeiro objeto desenhado."""
        self._ylim = (float(ymin), float(ymax))
        for objeto in self.objetos:
            if hasattr(objeto, "GetYaxis"):
                eixo_y = objeto.GetYaxis()
                if eixo_y:
                    eixo_y.SetRangeUser(*self._ylim)

    def legend(self, *_, **kwargs):
        """Draw a wide, legible legend in the upper plotting area."""
        fontsize = kwargs.get("fontsize", 0)
        if not hasattr(self, "_ylim"):
            maximo = max((obj.GetMaximum() for obj in self.objetos if hasattr(obj, "GetMaximum")), default=0.0)
            if maximo > 0:
                self.set_ylim(0.0, 1.35 * float(maximo))
        # Align the legend horizontally with the pad's internal data frame.
        x_min = float(self.pad.GetLeftMargin())
        x_max = 1.0 - float(self.pad.GetRightMargin())
        n_entries = sum(bool(getattr(obj, "GetTitle", lambda: "")()) for obj in self.objetos)
        y_min = 0.90 if n_entries <= 1 else 0.78
        objetos_com_rotulo = [obj for obj in self.objetos if getattr(obj, "GetTitle", lambda: "")()]
        legend = self.pad.BuildLegend(x_min, y_min, x_max, 0.98)
        if legend:
            for entrada in list(legend.GetListOfPrimitives()):
                objeto = entrada.GetObject()
                if objeto and objeto.InheritsFrom("TGraphAsymmErrors"):
                    legend.GetListOfPrimitives().Remove(entrada)
        # Preserve legend labels while suppressing ROOT's automatic plot title.
        for objeto in objetos_com_rotulo:
            objeto.SetTitle("")
        if legend:
            tamanho = max(0.025, min(0.06, float(fontsize) / 240.0)) if fontsize else 0.04
            legend.SetTextSize(tamanho)
        self.legend_obj = legend


class RootFigure:
    def __init__(self, nrows, ncols):
        self.canvas = ROOT.TCanvas("c", "FIS01214", 1200, 800)
        self.canvas.Divide(ncols, nrows)
        self.axes = [RootAxis(self.canvas.cd(i + 1), i) for i in range(nrows * ncols)]

    def suptitle(self, texto, **_):
        self.canvas.SetTitle(str(texto))

    def tight_layout(self, **_):
        return None

    def colorbar(self, objeto, ax=None, label=None, **_):
        if objeto:
            if ax is not None:
                ax.pad.SetRightMargin(0.20)
            eixo_z = objeto.GetZaxis()
            eixo_z.SetTitle(str(label or ""))
            eixo_z.SetTitleSize(0.05)
            eixo_z.SetLabelSize(0.04)

    def savefig(self, destino, **_):
        destino = Path(destino)
        destino.parent.mkdir(parents=True, exist_ok=True)
        self.canvas.Modified()
        self.canvas.Update()
        self.canvas.SaveAs(str(destino))
        # Preserve a vector render alongside the raster output for notebook embedding.
        if destino.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            self.canvas.SaveAs(str(destino.with_suffix(".svg")))


class RootPlot:
    def __init__(self):
        self._last_figure = None

    def subplots(self, nrows=1, ncols=1, squeeze=True, **_):
        figura = RootFigure(nrows, ncols)
        self._last_figure = figura
        eixos = np.asarray(figura.axes, dtype=object).reshape(nrows, ncols)
        if squeeze and nrows == 1 and ncols == 1:
            eixos = eixos[0, 0]
        elif squeeze and nrows == 1:
            eixos = eixos[0]
        elif squeeze and ncols == 1:
            eixos = eixos[:, 0]
        return figura, eixos

    def show(self):
        if self._last_figure is not None:
            self._last_figure.canvas.Draw()
            display(self._last_figure.canvas)
            return self._last_figure.canvas
        return None


plt = RootPlot()
