import numpy as np
from numpy import pi
import pyqg
import time
from pyqg.diagnostic_tools import spec_var

tmax = 5.
dt = 0.001
nsteps = int(tmax/dt)

# the model object
m = pyqg.BTModel(L=2.*pi, nx=256, tmax=tmax,
        beta=0., H=1., rek=0., rd=None, dt=dt,
        twrite=np.inf, taveint=np.inf, ntd=1)

# McWilliams 84 IC condition
fk = m.wv != 0
ckappa = np.zeros_like(m.wv2)
ckappa[fk] = np.sqrt( m.wv2[fk]*(1. + (m.wv2[fk]/36.)**2) )**-1

nhx, nhy = m.wv2.shape

Pi_hat = np.random.randn(nhx, nhy)*ckappa +1j*np.random.randn(nhx,nhy)*ckappa

Pi = m.ifft( Pi_hat[np.newaxis] )
Pi = Pi - Pi.mean()
Pi_hat = m.fft( Pi )
KEaux = spec_var( m, m.filtr*m.wv*Pi_hat )

pih = ( Pi_hat * np.sqrt(0.5/KEaux) )
qih = -m.wv2*pih
qi = m.ifft(qih)
m.set_q(qi)


t = time.time()
# run the model
m.run()

elapsed = (time.time() - t)/nsteps*1000
print('Time per time-step:  %.3f ms' %elapsed)

# import matplotlib.pyplot as plt
# plt.figure(figsize=(10, 4))
# plt.subplot(121)
# plt.pcolormesh(m.x-pi, m.y-pi, np.squeeze(qi[0,]).T )
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("vorticity @ t=0")
# plt.axis("square")
# plt.subplot(122)
# plt.pcolormesh(m.x-pi, m.y-pi, np.squeeze(m.q[0,]).T )
# plt.axis("square")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("vorticity @ t= %.2f" %m.t)
# plt.savefig("pyqg_n"+str(nhx)+".png", dpi=400)
