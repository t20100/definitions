
'''Writes a NeXus HDF5 file using h5py'''

import h5py    # HDF5 support

print "Write a NeXus HDF5 file"
fileName = "prj_test.nexus.hdf5"
timestamp = "2010-10-18T17:17:04-0500"

# prepare the data
f = open('input.dat',  'r')
TWO_COLUMNS = f.read()
f.close()

data = {'mr': [], 'I00': []}
buffer = TWO_COLUMNS.strip().split("\n")
for row in buffer:
    (x, y) = row.split()
    data['mr'].append(float(x))
    data['I00'].append(int(y))

# create the HDF5 NeXus file
f = h5py.File(fileName, "w")
f.attrs['file_name'] = fileName
f.attrs['file_time'] = timestamp
f.attrs['instrument'] = "APS USAXS at 32ID-B"
f.attrs['creator'] = "$Id$"
f.attrs['NeXus_version'] = "4.3.0"
f.attrs['HDF5_Version'] = h5py.version.hdf5_version
f.attrs['h5py_version'] = h5py.version.version

nxentry = f.create_group("entry")
nxentry.attrs["NX_class"] = "NXentry"   # identify NeXus base class

nxdata = nxentry.create_group("mr_scan")
nxdata.attrs["NX_class"] = "NXdata"   # identify NeXus base class

mr = nxdata.create_dataset("mr", data=data['mr'])
mr.attrs['units'] = "degrees"
mr.attrs['primary'] = "1"    # tell NeXus this is X axis for plotting

i00 = nxdata.create_dataset("I00", data=data['I00'])
i00.attrs['units'] = "counts"
i00.attrs['signal'] = "1"    # tell NeXus this is Y axis for plotting

# be CERTAIN to close the file
f.close()
print "wrote file:", fileName
