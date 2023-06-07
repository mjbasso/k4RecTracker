#include "TFile.h"
#include "TGraph.h"
#include "TMultiGraph.h"
#include "TString.h"
#include "TTreeReader.h"
#include "TTreeReaderArray.h"
#include "TVector3.h"

#include <cstdlib>

void quick_plot() {

    TFile* f = TFile::Open("digi.root");
    TTreeReader r("events", f);

    gROOT->SetBatch(1);
    TCanvas c = TCanvas("", "", 800, 800);

    TTreeReaderArray<Double_t> simx(r, "ARC_HITS.position.x");
    TTreeReaderArray<Double_t> simy(r, "ARC_HITS.position.y");
    TTreeReaderArray<Double_t> simz(r, "ARC_HITS.position.z");
    TTreeReaderArray<Double_t> recx(r, "ARC_DIGI_HITS.position.x");
    TTreeReaderArray<Double_t> recy(r, "ARC_DIGI_HITS.position.y");
    TTreeReaderArray<Double_t> recz(r, "ARC_DIGI_HITS.position.z");

    int index = -1;
    TVector3 simvec3, recvec3;
    TGraph simg, recg;
    while (r.Next()) {
        index++;
        if (simx.IsEmpty()) continue;
        simg = TGraph(simx.GetSize());
        for (std::size_t i = 0; i < simx.GetSize(); i++) {
            simvec3 = TVector3(simx.At(i), simy.At(i), simz.At(i));
            simg.SetPoint(i, simvec3.Eta(), simvec3.Phi());
        }
        recg = TGraph(recx.GetSize());
        for (std::size_t i = 0; i < recx.GetSize(); i++) {
            recvec3 = TVector3(recx.At(i), recy.At(i), recz.At(i));
            recg.SetPoint(i, recvec3.Eta(), recvec3.Phi());
        }
        simg.SetMarkerColor(kRed);
        simg.SetLineWidth(0);
        recg.SetMarkerColor(kBlue);
        recg.SetLineWidth(0);
        TMultiGraph mg = TMultiGraph();
        mg.Add(&simg);
        mg.Add(&recg);
        mg.Draw("AP");
        mg.SetTitle(TString::Format("Event %d", index));
        mg.GetXaxis()->SetTitle("#eta");
        mg.GetYaxis()->SetTitle("#phi [rad]");
        c.SaveAs(TString::Format("%d.pdf", index));
    }
}
