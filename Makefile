MAKEFLAGS += --no-print-directory
CERNBOX := https://cernbox.cern.ch/remote.php/dav/public-files/as7zVSKFeOVL9DP

make:
	@ mkdir -p build install ; \
	cd build ; \
	source /cvmfs/sw.hsf.org/key4hep/setup.sh ; \
	cmake .. -DCMAKE_INSTALL_PREFIX=../install ; \
	make install -j4 ; \
	cd .. ; \
	export LD_LIBRARY_PATH=${CURDIR}/install/lib:${CURDIR}/install/lib64:${CURDIR}/k4geo/install/lib:${CURDIR}/k4geo/install/lib64:$$LD_LIBRARY_PATH ; \
	export PYTHONPATH=${CURDIR}/install/python:$$PYTHONPATH ; \
	printf "#!/bin/bash\nsource /cvmfs/sw.hsf.org/key4hep/setup.sh\nexport LD_LIBRARY_PATH=${CURDIR}/install/lib:${CURDIR}/install/lib64:${CURDIR}/k4geo/install/lib:${CURDIR}/k4geo/install/lib64:\$$LD_LIBRARY_PATH\nexport PYTHONPATH=${CURDIR}/install/python:\$$PYTHONPATH\n" > ${CURDIR}/setup.sh ; \
	chmod +x ${CURDIR}/setup.sh
get_data:
	@ mkdir -p data ; \
	wget -P data ${CERNBOX}/CLD_with_ARC_fullsim.root ${CERNBOX}/CLD_with_ARC_trackReco_edm4hep.root

.PHONY: clean
clean:
	@ (rm -r build install && rm setup.sh) || true
