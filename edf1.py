import numpy as np 
import mne 
import matplotlib.pyplot as plt 
import os
import time

#PSG de personas 2,6 & 9
reading_time = time.time()
raw_1 = mne.io.read_raw_edf('SC4022E0-PSG.edf', preload=True)
raw_2 = mne.io.read_raw_edf('SC4062E0-PSG.edf', preload=True)
raw_3 = mne.io.read_raw_edf('SC4092E0-PSG.edf', preload=True)
print("--------------------------------------------")
print("3 raw leidos en %s segundos || " %(time.time()-reading_time))

#Extraer data, frecuencia de muestreo y nombre de canales 
data_1, sf_1, chan_1 = raw_1._data, raw_1.info['sfreq'], raw_1.info['ch_names']
data_2, sf_2, chan_2 = raw_2._data, raw_2.info['sfreq'], raw_2.info['ch_names']
data_3, sf_3, chan_3 = raw_3._data, raw_3.info['sfreq'], raw_3.info['ch_names']



raw_temp1=raw_1.copy()
raw_temp2=raw_1.copy()
print(raw_temp1.ch_names)


##Escoger canales
#raw1
eeg_Fpz = raw_temp1.pick_channels(['EEG Fpz-Cz'])
eeg_Oz = raw_temp2.pick_channels(['EEG Pz-Oz'])

#raw2
raw2_temp1 = raw_2.copy()
raw2_temp2 = raw_2.copy()
eeg2_Fpz = raw2_temp1.pick_channels(['EEG Fpz-Cz'])
eeg2_Oz = raw2_temp2.pick_channels(['EEG Pz-Oz'])

#raw3
raw3_temp1 = raw_3.copy()
raw3_temp2 = raw_3.copy()
eeg3_Fpz = raw3_temp1.pick_channels(['EEG Fpz-Cz'])
eeg3_Oz = raw3_temp2.pick_channels(['EEG Pz-Oz'])


#Leer anotaciones de Hypnogramas
annot_1 = mne.read_annotations('SC4022EJ-Hypnogram.edf')
annot_2 = mne.read_annotations('SC4062EC-Hypnogram.edf')
annot_3 = mne.read_annotations('SC4092EC-Hypnogram.edf')


annotation_desc_2_event_id = {'Sleep stage W': 1,
                              'Sleep stage 1': 2,
                              'Sleep stage 2': 3,
                              'Sleep stage 3': 4,
                              'Sleep stage 4': 4,
                              'Sleep stage R': 5}


#Crop 20min antes y despues de dormir

annot_1.crop(annot_1[1]['onset'] - 20*60,
      annot_1[-2]['onset'] + 20*60)

annot_2.crop(annot_2[1]['onset'] - 20*60,
      annot_2[-2]['onset'] + 20*60)

annot_3.crop(annot_3[1]['onset'] - 20*60,
      annot_3[-4]['onset'] + 20*60)

#Setear annotaciones

raw_1.set_annotations(annot_1, emit_warning=False)
raw_2.set_annotations(annot_2, emit_warning=False)  
raw_3.set_annotations(annot_3, emit_warning=False)  

#Extraer eventos de 30s a partir de anotaciones
events1, _ = mne.events_from_annotations(
    raw_1, event_id=annotation_desc_2_event_id, chunk_duration=30.)

events2, _ = mne.events_from_annotations(
    raw_2, event_id=annotation_desc_2_event_id, chunk_duration=30.)

events3, _ = mne.events_from_annotations(
    raw_3, event_id=annotation_desc_2_event_id, chunk_duration=30.)

#Crear nuevo event_id que unifica etapas 3 y 4 
event_id = {'Sleep stage W': 1,
            'Sleep stage 1': 2,
            'Sleep stage 2': 3,
            'Sleep stage 3/4': 4,
            'Sleep stage R': 5}


#plot Fpz-Cz de cada persona a partir de anotaciones de eventos
fig_1 = mne.viz.plot_events(events1, event_id=event_id,
                          sfreq=eeg_Fpz.info['sfreq'],
                          first_samp=events1[0,0],show=False)

fig_2 = mne.viz.plot_events(events2, event_id=event_id,
                          sfreq=eeg2_Fpz.info['sfreq'],
                          first_samp=events2[0,0],show=False)

fig_3 = mne.viz.plot_events(events3, event_id=event_id,
                          sfreq=eeg3_Fpz.info['sfreq'],
                          first_samp=events3[0,0],show=False)

#Mantener codigo de colores para siguientes plots.
stage_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']            


#Extraer epocas de 30s
tmax_1 = 30. - 1. / raw_1.info['sfreq']
tmax_2 = 30. - 1. / raw_2.info['sfreq']
tmax_3 = 30. - 1. / raw_3.info['sfreq'] 

epochs1 = mne.Epochs(raw=eeg_Fpz, events=events1,
                          event_id=event_id, tmin=0., tmax=tmax_1, baseline=None)

epochs2 = mne.Epochs(raw=eeg2_Fpz, events=events2,
                          event_id=event_id, tmin=0., tmax=tmax_2, baseline=None)

epochs3 = mne.Epochs(raw=eeg3_Fpz, events=events3,
                          event_id=event_id, tmin=0., tmax=tmax_3, baseline=None)

print(epochs1)

##################
#Plot some epochs
epochs1_data=epochs1.get_data()#darray of shape (929,1,3000)
epochs2_data=epochs2.get_data()
epochs3_data=epochs3.get_data()
L=np.arange(3000) #samples per epoch
#print(len(epochs1_data[0,0,:]))

fig1, axs1 = plt.subplots(nrows=3,ncols=2)
axs1[0,0].plot(L/sf_1, epochs1_data[0,0,:])  #why 0.0001
axs1[0,0].set_xlim((0,30)) #epoch 0 
#axs1[0,0].set_ylim((-100*10**-7,100*10**-7))
axs1[0,0].set_title('??poca 1, Persona 2 (Fpz_Cz)') #No superponer titulos de estos dos plots
axs1[0,0].set_xlabel('tiempo [s]')
axs1[0,0].set_ylabel('voltaje [uV]')

axs1[1,0].plot(L/sf_2, epochs2_data[0,0,:])
axs1[1,0].set_xlim((0,30))
axs1[1,0].set_title('??poca 1, Persona 6')
axs1[1,0].set_xlabel('tiempo [s]')
axs1[1,0].set_ylabel('voltaje [uV]')

axs1[0,1].plot(L/sf_1,epochs1_data[1,0,:])
axs1[0,1].set_xlim((0,30)) #epoch 2 
axs1[0,1].set_title('??poca 2, Persona 2')
axs1[0,1].set_xlabel('tiempo [s]')
axs1[0,1].set_ylabel('voltaje [uV]')

axs1[1,1].plot(L/sf_2, epochs2_data[1,0,:])
axs1[1,1].set_xlim((0,30)) #epoch 2 
axs1[1,1].set_title('??poca 2, Persona 6')
axs1[1,1].set_xlabel('tiempo [s]')
axs1[1,1].set_ylabel('voltaje [uV]')

axs1[2,0].plot(L/sf_3,epochs3_data[0,0,:])
axs1[2,0].set_xlim((0,30)) #epoch 2 
axs1[2,0].set_title('??poca 1, Persona 9')
axs1[2,0].set_xlabel('tiempo [s]')
axs1[2,0].set_ylabel('voltaje [uV]')

axs1[2,1].plot(L/sf_3, epochs3_data[1,0,:])
axs1[2,1].set_xlim((0,30)) #epoch 2 
axs1[2,1].set_title('??poca 2, Persona 9')
axs1[2,1].set_xlabel('tiempo [s]')
axs1[2,1].set_ylabel('voltaje [uV]')


fig1.tight_layout()

plt.show()



#Visualizar densidad de potencia espectral (PSD) de las tres personas
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)

stages = sorted(event_id.keys())
for ax, title, epochs in zip([ax1, ax2, ax3],
                             ['Subject 2', 'Subject 6', 'Subject 9'],
                             [epochs1, epochs2, epochs3]):

    for stage, color in zip(stages, stage_colors):
        epochs[stage].plot_psd(area_mode=None, color=color, ax=ax,
                               fmin=0.1, fmax=20., show=False,
                               average=True, spatial_colors=False)
    ax.set(title=title, xlabel='Frequency (Hz)')
ax2.set(ylabel='??V^2/Hz (dB)')
ax2.legend(ax2.lines[2::3], stages)

plt.tight_layout()
plt.show()


