"""
    A collection of python for generating spikeinterface compatible probe maps

"""
import pandas as pd
import probeinterface
from probeinterface.plotting import plot_probe
from probeinterface.probegroup import ProbeGroup


def gen_masmanidis_probe(probe_wiring, visualize=False):
    """
    gen_masmanidis_probe is a simple function that takes the output of the
    masmanidis's labs channel map creators in matlab (represented as a matrix)
    and spits out a probeinterface compatible version of those maps that can be
    used for subsequent spike sorting

    Args:
        probe_wiring (numpy array): Up to 5 columns define each masmanidis probe
        array. By design they follow the same convention as follows

        col1 : channel number on probe
        col2 : x coordinate of each channel
        col3 : y coordinate of each channel (always zero)
        col4 : z coordinate of each channel (aka, depth)
        col5 : shaft number, usually a binary value of 1-4 depending on the
        probe type

    Returns:
        probeinterface object: This is a group object as defined by the
        probeinterface ProbeGroup class. Basically you can then write from this
        format to whatever format is convenient for your spike sorting needs. I
        typically do prb, but you can also use probeinterface's own format
    """

    #load in the relevant x,y,z,shank data into a dataframe
    new_probe = pd.DataFrame({
        'x': probe_wiring[:, 1],
        'y': probe_wiring[:, 3],
        'shank_ids': probe_wiring[:, 4] - 1})

    #Find out how many channels you have
    ch_num = len(new_probe)

    #write basic information for probes. MAGIC - these are taken from the
    #masmanidis catalog
    new_probe.loc[:, 'contact_shapes'] = 'circle'
    new_probe.loc[:, 'radius'] = 10

    #create a probeinterface object from the data frame
    my_probe = probeinterface.Probe.from_dataframe(new_probe)

    #optional, plot a map of the probe
    if visualize:
        my_probe.create_auto_shape()
        plot_probe(my_probe)

    #each probe needs a set of channel indices
    my_probe.set_device_channel_indices(range(ch_num))

    #create a probe group object, called probe
    probe = ProbeGroup()
    probe.add_probe(my_probe)
    return probe
