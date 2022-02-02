#FROM hysds1/pge-base-conda-isce2:20201212
#FROM hysds/isce2:latest-es1
FROM cae-artifactory.jpl.nasa.gov:16001/gov/nasa/jpl/nisar/sds/pcm/nisar_ade:r1.3
#FROM artifactory.com/nisar_ade:latest

ENV HOME=/home/jovyan \
    CONDA_DIR=/opt/conda

USER root
RUN $CONDA_DIR/bin/conda install -y nb_conda_kernels

# ref: https://stackoverflow.com/questions/47955200/specific-package-version-with-conda-forge
# search for all versions
#conda search isce2 --channel conda-forge
# ref: https://anaconda.org/conda-forge/isce2
# install isce 2.4.2
# save this for late upgrade
#RUN $CONDA_DIR/bin/conda install -c conda-forge isce2=2.4.2

# 20210616, temp fix for error as described in
# https://github.com/psf/black/issues/1628
RUN $CONDA_DIR/bin/pip install -U click

RUN $CONDA_DIR/bin/pip install 'ipykernel<5.0.0'
RUN chmod 4777 $HOME

USER jovyan

# ONLY TOUCH IF YOU NEED MORE RECENT VERSION, OTHERWISE DON'T TOUCH!!
# RUN cd $HOME \
#     && git clone https://github.com/hysds/notebook_pge_wrapper.git \
#     && cd notebook_pge_wrapper \
#     && $CONDA_DIR/bin/pip install -e .

# have a local isce2/topsStack with fetchOrbit-asf.py
# under $HOME/isce2/topsStack
RUN mkdir -p $HOME/isce2
RUN cp -ai /opt/isce2/src/isce2/contrib/stack/topsStack $HOME/isce2
RUN mv $HOME/isce2/topsStack/fetchOrbit.py $HOME/isce2/topsStack/fetchOrbit.py.ori
COPY tool/barn/fetchOrbit-asf.py $HOME/isce2/topsStack
RUN ln -sf $HOME/isce2/topsStack/fetchOrbit-asf.py $HOME/isce2/topsStack/fetchOrbit.py

COPY . $HOME/topsstack_hamsar

# installing user defined dependencies
RUN $CONDA_DIR/bin/papermill $HOME/topsstack_hamsar/docker/requirements.ipynb /tmp/requirements_output.ipynb --log-output

WORKDIR $HOME

CMD ["/bin/bash", "--login"]
