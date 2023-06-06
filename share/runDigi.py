from Gaudi.Configuration import *
from Configurables import ApplicationMgr

from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")

from Configurables import k4DataSvc
dataservice = k4DataSvc("EventDataSvc", input = vars().get("input", "data/arcsim_kaon+_edm4hep.root"))

from Configurables import PodioInput
podioinput = PodioInput("PodioInput", collections = ["ARC_HITS"], OutputLevel = DEBUG)

from Configurables import ARCdigitizer
arc_digitizer = ARCdigitizer("ARCdigitizer",
    inputSimHits = "ARC_HITS",
    outputDigiHits = "ARC_DIGI_HITS",
    detectorCompact = "k4geo/FCCee/compact/CLD_ARC/arc_full_v0.xml"
)

from Configurables import PodioOutput
podiooutput = PodioOutput("PodioOutput", filename = vars().get("output", "digi.root"), OutputLevel = DEBUG)
podiooutput.outputCommands = ["keep *"]

# CPU information
from Configurables import AuditorSvc, ChronoAuditor
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
arc_digitizer.AuditExecute = True
podiooutput.AuditExecute = True

from Configurables import EventCounter
event_counter = EventCounter('event_counter')
event_counter.Frequency = 1

ApplicationMgr(
    TopAlg = [
        event_counter,
        podioinput,
        arc_digitizer,
        podiooutput
    ],
    EvtSel = 'NONE',
    EvtMax = 10,
    ExtSvc = [geoservice, dataservice]
)
