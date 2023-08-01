
#plots data from seedavg.py simulation

import numpy as np
from matplotlib import pyplot as plt
from seedavg import *
import seaborn as sns
import scipy.stats
nrows=4
Data=np.load("recfolder/Data_rec.npy",allow_pickle=True)      #change back to oldData.npy
Caro=Car[:]
Data=Data[:,:,:]
print(Car,len(Car))
DatShape=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],1
DatShape2=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],nrows


Dat=np.ones(DatShape)*-1      
Dat2=np.ones(DatShape2)*-1 
print(np.shape(Dat2))

for a in range(len(Data)):
    for b in range(len(Data[0])):
        for c in range(len(Data[0,0])):
            for d in range(len(Data[0,0,0])):
                for e in range(len(Data[0,0,0,0])):     #build proper Tensor
                    Dat[a,b,c,d,e]=Data[a,b,c,d,e][1]      #full recordings, not saved anymore    
                    Dat2[a,b,c,d,e,:]=Data[a,b,c,d,e][4],Data[a,b,c,d,e][2],Data[a,b,c,d,e][13],Data[a,b,c,d,e][10] 
#[-1,-1,a.power(location="difference"),a.power(location="soma"),a.freq(pop=net.pyr),a.freq(pop=net.bas),a.freq(pop=net.olm),a.rasterpower(),r["nTE_XY"],r] 
                    #Dat2[a,b,c,d,e,:]=[Data[a,b,c,d,e][6]["p_value_XY"],Data[a,b,c,d,e][6]["p_value_YX"]]  #theta and gamma power and potentially so much more!
dat=np.array(Dat,dtype=float)
dat2=np.array(Dat2,dtype=float)



imax=len(dat2[0,0])
jmax=len(dat2[0,0,0])
kmax=len(dat2[0,0,0,0])
import matplotlib.colors

def freqandgamma(): #plots avg over seeds, freq and gamma dependent on factor krec or kext, for rec and ext
    d=dat2[0,:,:,0,:,:]
    sh=np.shape(d)
    print(sh)
    da=np.average(d,axis=0)
    #now you have shape(da)=(seeds,Ca,rec/ext,f/gamma)
    fig, ax = plt.subplots(nrows=nrows, ncols=sh[2], figsize=(10, 10)) #if Car is len 1, ax has to be 1 modal
    for nn in range(sh[2]):
        ax[2].set_xlabel(r'$k_{rec}$')
    ax[0].set_ylabel('frequency')
    ax[1].set_ylabel(r'LFP $\gamma$')
    ax[2].set_ylabel(r'$\chi$ (Basket)')#raster $\gamma$')
    ax[3].set_ylabel(r'$\chi$')
    #for j in range(sh[2]):          
    #    ax[0].set_title(str(5.3*Ear[j])+"ms")
    #ax[0].set_title(r'$\tau_2=$ '+str(5.3*Ear[0])+"ms")

    for i in range(sh[3]):
        for j in range(sh[2]):
            ax[i].plot(Caro,da[:,j,i],'-o', color="black", alpha=0.5, linewidth=1, markersize=4)
            for k in range(sh[0]):
                ax[i].scatter(Caro,d[k,:,j,i],color="black",s=1)
            ax[i].errorbar(Caro,np.mean(d[:,:,j,i],axis=0),np.var(d[:,:,j,i],axis=0),color="black",linewidth=.4)
            if i==0:
                ax[i].set_yscale('log')
                ax[i].set_ylim([1,300])
            if i==1:
                ax[i].set_ylim([-0.1,20])
            if i==2:
                pass
                #ax[i].set_yscale('log')
                #ax[i].set_ylim([0.00001,5])
            if i==3:
                pass
                #ax[i].set_yscale('log')
                #ax[i].set_ylim([0.00001,1.0])

            #ax[i,j].set_xscale('log')
    plt.show()

freqandgamma()

def difs():
    dif2=dat2[1]-dat2[0]
    for i in range(imax):#rec, each a different figure
        fig=plt.figure(i,figsize=(3,3),dpi=80)
        for j in range(jmax):
            for k in range(kmax):
                #j is ext, row? in subplot
                #k is soma, column in subplot
                pows=np.average(dif2,axis=1)
                pows_std=np.std(dif2,axis=1)/(len(dif2[0])-1)**.5 #sample error estimate or whatever
                x=np.arange(len(pows))/1.+1.
                cmap = plt.cm.rainbow
                norm = matplotlib.colors.Normalize(vmin=2, vmax=4)
                #jlist=1+np.arange(0,4)*0.25
                #klist=1+np.arange(0,4)*0.25
                plt.scatter(j,k,color=cmap(norm(pows[i,j,k,1])),label="gamma power(30-100 Hz)")#first index=0 means control trial, last index=1 means gamma
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # only needed for matplotlib < 3.1
        fig.colorbar(sm)
        plt.title("rec="+str(i))
    plt.show()

def allplots(boxplot=True):

    pows=np.average(dat2,axis=1)
    pows_std=np.std(dat2,axis=1)/(len(dat2[0])-1)**.5 #sample error estimate or whatever
    x=np.arange(len(pows))/1.
    for k in range(kmax):#rec, each a different figure #E
        fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(10, 10))
        for nn in range(4):
            ax[3,nn].set_xlabel('control vs. ketamine')
            ax[nn,0].set_ylabel('gamma power')
        for j in range(jmax):#all #D
            for i in range(imax):#rec #C
                #plt.subplot(imax,jmax,1+i+imax*j)
                if boxplot==False:
                    ax[i,j].plot(x,pows[:,i,j,k,1],label="gamma power(30-100 Hz)", color="black")#first index=0 means control trial, last index=1 means gamma
                    ax[i,j].errorbar(x=x,y=pows[:,i,j,k,1],yerr=pows_std[:,i,j,k,1],color="grey",fmt=".")
                else:
                    ax[i,j].boxplot([dat2[0,:,i,j,k,1],dat2[1,:,i,j,k,1]],positions=[0,1])
                sns.stripplot(data=[dat2[0,:,i,j,k,1],dat2[1,:,i,j,k,1]], jitter=.08, color='black', ax=ax[i,j],size=3)
                ax[i,j].set_ylim([1.5,4.5])
                #plt.xlabel("ctrl. vs. ket.")
                #ax[i,j].text(0.2,4.3,str(i)+str(j)+str(k))#rec,ext,som=xxx
                ax[i,j].text(-0.4,4.3,"rec:"+str(cpfp(i,j,k)[0])+", all:"+str(cpfp(i,j,k)[1]))
                presult=scipy.stats.ttest_rel(a=dat2[0,:,i,j,k,1],b=dat2[1,:,i,j,k,1], axis=0)
                ax[i,j].text(-0.4,4.1,"p="+"{:.1e}".format(presult.pvalue/2.))
        plt.subplots_adjust(left=None, bottom=None, right=1., top=1., wspace=None, hspace=None)
    
    fig.tight_layout(pad=2.0)
    plt.show()

#allplots()

#transform into r readable format (CSV?)
csvtrafo=False
if csvtrafo:
    gc=[]
    gk=[]
    rec=[]
    ext=[]
    for b in range(nB):#seed
        for c in range(nC):#rec
            for d in range(nD):#ext           check this again, questionable
                gc.append(dat2[0,b,c,d,0][1])
                gk.append(dat2[1,b,c,d,0][1])
                rec.append(cpfp(c,d,1)[0])
                ext.append(cpfp(c,d,1)[1])

    import pandas as pd
    df=pd.DataFrame({})
    df["gammacontrol"]=gc
    df["gammaketamine"]=gk
    df["deltagamma"]=gk-gc
    df["rec"]=rec
    df["ext"]=ext
    df.to_csv('oldData.csv', index=True)
