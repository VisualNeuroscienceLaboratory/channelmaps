"""
A simple function for translating .json files written using probe interface to a
.mat file that can serve as a channel map in kilosort2-onwards

Typical usage example:


  on the command line:
    python json2ks2 filename output_directory
  
  after importing library:
    json2ks2(filename,sampling_rate = 30000, outdir = './'):
  

"""
import argparse
import os
import json
import numpy as np
import scipy.io as sio


def json2ks2(filename, sampling_rate=30000, outdir='./'):
    """
    json2ks2 main function to convert a json file to a .mat file

    Args:
        filename (str): filename (including path) of the .json file
        sampling_rate (int, optional): sampling rate of 
        the acquisition system. Defaults to 30000.
        outdir (str, optional): output directory where you will write the file. Defaults to './'.

    Returns:
        list: a list of dictionaries, one for each probe in the json file
    """
    snippet = filename.split('/')[-1]
    # Opening JSON file
    fid = open(filename, encoding='UTF-8')

    # returns JSON object as # a dictionary
    data = json.load(fid)

    if len(data['probes']) == 1:
        outname_list = [os.path.join(outdir, snippet + '.mat')]
    else:
        outname_list = [
            os.path.join(outdir, snippet + '_probe_' + str(index + 1) + '.mat')
            for index, _ in enumerate(data['probes'])
        ]
    probe_list = []

    for index, probe in enumerate(data['probes']):
        output = {}
        pos = np.asarray(probe['contact_positions'])
        num_channels = np.max(np.shape(pos))

        output['connected'] = np.ones((num_channels, 1), dtype=bool)
        output['chanMap'] = np.arange(1, num_channels + 1)
        output['chanMap0ind'] = output['chanMap'] - 1
        output['xcoords'] = pos[:, 0]
        output['ycoords'] = pos[:, 1]
        shank_ids = np.asarray(probe['shank_ids']).astype(float)
        shank_ids = shank_ids - np.min(shank_ids) + 1
        output['kcoords'] = shank_ids
        output['fs'] = sampling_rate
        probe_list.append(output)
        sio.savemat(outname_list[index], output)
    return probe_list


def main():
    """
    main command line function to convert a given json file to a kilosort
    friendly format, see above for typical usage.
    """
    #parse command line inputs
    parser = argparse.ArgumentParser(description='Convert json files to .mat files that can be used in kilosort')
    parser.add_argument('file_in',metavar='file_in',type=str,help='file location')
    parser.add_argument('--outpath',metavar='outdir',type=str,help='location where the output file will be saved',default = './',required=False)
    parser.add_argument('--sampling_rate',metavar='sampling_rate',type=int,help='sampling rate of acquisition system',default=30000, required=False)
    args = parser.parse_args()

    #main function
    json2ks2(args.file_in,outdir=args.outpath,sampling_rate=args.sampling_rate)

if __name__ == "__main__":
    main()
