import numpy as np 
#from visbrain.gui import Sleep
import mne 
import matplotlib.pyplot as plt 
import os
import time
#import plotly.graph_objects as go


#subject 2,6 & 9
reading_time = time.time()
raw_1 = mne.io.read_raw_edf('SC4022E0-PSG.edf', preload=True)
raw_2 = mne.io.read_raw_edf('SC4062E0-PSG.edf', preload=True)
raw_3 = mne.io.read_raw_edf('SC4092E0-PSG.edf', preload=True)
print("3 raw leidos en %s segundos --- " %(time.time()-reading_time))

#Extract data, sampling frequency and channels names
data_1, sf_1, chan_1 = raw_1._data, raw_1.info['sfreq'], raw_1.info['ch_names']
data_2, sf_2, chan_2 = raw_2._data, raw_2.info['sfreq'], raw_2.info['ch_names']
data_3, sf_3, chan_3 = raw_3._data, raw_3.info['sfreq'], raw_3.info['ch_names']

#Sleep(data=data, sf=sf, channels=chan).show()
#raw_win=raw.crop(tmax=100)
#ch_FPz=raw.info['chs']
#print(ch_FPz)

#events=mne.find_events(raw)
#epochs = mne.Epochs(raw, events, tmin=0, tmax=100)

raw_temp1=raw_1.copy()
raw_temp2=raw_1.copy()
print(raw_temp1.ch_names)
#raw_temp.pick_channels([FPz])
eeg_Fpz=raw_temp1.pick_channels(['EEG Fpz-Cz'])
eeg_Oz=raw_temp2.pick_channels(['EEG Pz-Oz'])
time=np.arange(len(eeg_Fpz[0]))
#eeg_Fpz.plot()
#plt.ylim([-100,100])
# plt.show()



raw2_temp1=raw_2.copy()
raw2_temp2=raw_2.copy()
eeg2_Fpz=raw2_temp1.pick_channels(['EEG Fpz-Cz'])
eeg2_Oz=raw2_temp2.pick_channels(['EEG Pz-Oz'])
#time2=np.arange(len(eeg2_Fpz[0]))
#eeg2_Fpz.plot()
#plt.ylim([-100,100])


raw3_temp1=raw_3.copy()
raw3_temp2=raw_3.copy()
eeg3_Fpz=raw3_temp1.pick_channels(['EEG Fpz-Cz'])
eeg3_Oz=raw3_temp2.pick_channels(['EEG Pz-Oz'])



annot_1=mne.read_annotations('SC4022EJ-Hypnogram.edf')
annot_2=mne.read_annotations('SC4062EC-Hypnogram.edf')
annot_3=mne.read_annotations('SC4092EC-Hypnogram.edf')





#print(annot_1[1])
annotation_desc_2_event_id = {'Sleep stage W': 1,
                              'Sleep stage 1': 2,
                              'Sleep stage 2': 3,
                              'Sleep stage 3': 4,
                              'Sleep stage 4': 4,
                              'Sleep stage R': 5}


#20min antes y despues de dormir. To avoid class Imbalance

annot_1.crop(annot_1[1]['onset'] - 20*60,
			annot_1[-2]['onset'] + 20*60)

annot_2.crop(annot_2[1]['onset'] - 20*60,
			annot_2[-2]['onset'] + 20*60)

annot_3.crop(annot_3[1]['onset'] - 20*60,
			annot_3[-4]['onset'] + 20*60)

#os._exit(os.EX_OK)

raw_1.set_annotations(annot_1, emit_warning=False)
raw_2.set_annotations(annot_2, emit_warning=False)  
raw_3.set_annotations(annot_3, emit_warning=False)  

#extract 30s events from annotations. ?Bothchannel?
events1, _ = mne.events_from_annotations(
    raw_1, event_id=annotation_desc_2_event_id, chunk_duration=30.)
'''
events1_Fpz, _ = mne.events_from_annotations(
    eeg_Fpz, event_id=annotation_desc_2_event_id, chunk_duration=30.)
events1_Oz, _ = mne.events_from_annotations(
    eeg_Oz , event_id=annotation_desc_2_event_id, chunk_duration=30.)
'''

events2, _ = mne.events_from_annotations(
    raw_2, event_id=annotation_desc_2_event_id, chunk_duration=30.)
'''
events2_Fpz, _ = mne.events_from_annotations(
    eeg2_Fpz, event_id=annotation_desc_2_event_id, chunk_duration=30.)
events2_Oz, _ = mne.events_from_annotations(
    eeg2_Oz, event_id=annotation_desc_2_event_id, chunk_duration=30.)
'''
events3, _ = mne.events_from_annotations(
    raw_3, event_id=annotation_desc_2_event_id, chunk_duration=30.)
'''
events3_Fpz, _ = mne.events_from_annotations(
    eeg3_Fpz, event_id=annotation_desc_2_event_id, chunk_duration=30.)
events3_Oz, _ = mne.events_from_annotations(
    eeg3_Oz, event_id=annotation_desc_2_event_id, chunk_duration=30.)                          
'''

# create a new event_id that unifies stages 3 and 4
event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3/4': 4,
            'Sleep stage R': 5}


#plot every subject Fpz-Cz from event annotations .
fig_1 = mne.viz.plot_events(events1, event_id=event_id,
                          sfreq=eeg_Fpz.info['sfreq'],
                          first_samp=events1[0,0],show=False) #first_samp=events1[0, 0],show=False) ##from 2channel raw

fig_2 = mne.viz.plot_events(events2, event_id=event_id,
                          sfreq=eeg2_Fpz.info['sfreq'],
                          first_samp=events2[0,0],show=False)

fig_3 = mne.viz.plot_events(events3, event_id=event_id,
                          sfreq=eeg3_Fpz.info['sfreq'],
                          first_samp=events3[0,0],show=False)

# keep the color-code for further plotting
stage_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']            


#extract 30s epochs both Fpz-Cz and Pz-Oz channels?
tmax_1 = 30. - 1. / raw_1.info['sfreq']
tmax_2 = 30. - 1. / raw_2.info['sfreq']
tmax_3 = 30. - 1. / raw_3.info['sfreq']  # tmax in included

epochs1 = mne.Epochs(raw=eeg_Fpz, events=events1,
                          event_id=event_id, tmin=0., tmax=tmax_1, baseline=None)
'''
epochs1_Pz = mne.Epochs(raw=eeg_Fpz, events=events1,
                          event_id=event_id, tmin=0., tmax=tmax_1, baseline=None)
epochs1_Oz = mne.Epochs(raw=eeg_Oz, events=events1,
                          event_id=event_id, tmin=0., tmax=tmax_1, baseline=None)
'''
epochs2 = mne.Epochs(raw=eeg2_Fpz, events=events2,
                          event_id=event_id, tmin=0., tmax=tmax_2, baseline=None)
'''
epochs2_Pz = mne.Epochs(raw=eeg2_Fpz, events=events2,
                          event_id=event_id, tmin=0., tmax=tmax_2, baseline=None)
epochs2_Oz = mne.Epochs(raw=eeg2_Oz, events=events2,
                          event_id=event_id, tmin=0., tmax=tmax_2, baseline=None)
'''

epochs3 = mne.Epochs(raw=eeg3_Fpz, events=events3,
                          event_id=event_id, tmin=0., tmax=tmax_3, baseline=None)

print(epochs1)
'''
epochs3_Pz = mne.Epochs(raw=eeg3_Fpz, events=events3,
                          event_id=event_id, tmin=0., tmax=tmax_3, baseline=None)
epochs3_Oz = mne.Epochs(raw=eeg3_Oz, events=events3,
                          event_id=event_id, tmin=0., tmax=tmax_3, baseline=None)
'''

'''
temporary problem with scipy en plot_psd´
'''
# visualize Alice vs. Bob PSD by sleep stage.


fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)

# iterate over the subjects
stages = sorted(event_id.keys())
for ax, title, epochs in zip([ax1, ax2, ax3],
                             ['Alice', 'Bob', '33'],
                             [epochs1, epochs2, epochs3]):

    for stage, color in zip(stages, stage_colors):
        epochs[stage].plot_psd(area_mode=None, color=color, ax=ax,
                               fmin=0.1, fmax=20., show=False,
                               average=True, spatial_colors=False)
    ax.set(title=title, xlabel='Frequency (Hz)')
ax2.set(ylabel='µV^2/Hz (dB)')
ax2.legend(ax2.lines[2::3], stages)

plt.tight_layout()
plt.show()
 


