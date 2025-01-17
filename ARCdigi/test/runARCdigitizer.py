from Gaudi.Configuration import *
from Configurables import ApplicationMgr

from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
geoservice.detectors.append("k4geo/FCCee/CLD/compact/CLD_o3_v01/ARC_o1_v01.xml")

from Configurables import k4DataSvc
dataservice = k4DataSvc("EventDataSvc", input = vars().get("input", "data/CLD_with_ARC_fullsim.root"))

from Configurables import PodioInput
podioinput = PodioInput("PodioInput", collections = ["ARC_HITS"], OutputLevel = DEBUG)

from Configurables import ARCdigitizer
arc_digitizer = ARCdigitizer("ARCdigitizer",
    inputSimHits = "ARC_HITS",
    outputDigiHits = "ARC_DIGI_HITS"
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
