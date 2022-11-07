: from template

: $Id: MyExp2SynBB.mod,v 1.4 2010/12/13 21:27:51 samn Exp $ 
NEURON {
:  THREADSAFE
  POINT_PROCESS MyExp2SynBB
  RANGE tau1, tau2, e, i, g, Vwt, gmax
  NONSPECIFIC_CURRENT i
}

UNITS {
  (nA) = (nanoamp)
  (mV) = (millivolt)
  (uS) = (microsiemens)

}

PARAMETER {
  tau1=.1 (ms) <1e-9,1e9>
  tau2 = 10 (ms) <1e-9,1e9>
  e=0	(mV)
  gmax = 1e9 (uS)
  Vwt   = 0 : weight for inputs coming in from vector
}

ASSIGNED {
  v (mV)
  i (nA)
  g (uS)
  factor
  etime (ms)
}

STATE {
  A (uS)
  B (uS)
}

INITIAL {
  LOCAL tp

  Vwt = 0    : testing

  if (tau1/tau2 > .9999) {
    tau1 = .9999*tau2
  }
  A = 0
  B = 0
  tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
  factor = -exp(-tp/tau1) + exp(-tp/tau2)
  factor = 1/factor
}

BREAKPOINT {
  SOLVE state METHOD cnexp
  g = B - A
  if (g>gmax) {g=gmax}: saturation
  i = g*(v - e)
}

DERIVATIVE state {
  A' = -A/tau1
  B' = -B/tau2
}

NET_RECEIVE(weight (umho), F, D1, D2, tsyn (ms)) { : NET_RECEIVE: If there is net_send() an event that targets this mechanism, lines here are executed first. Skipped otherwise.
INITIAL {
: these are in NET_RECEIVE to be per-stream
        F = 1
        D1 = 1
        D2 = 1
        tsyn = t
: this header will appear once per stream
: printf("t\t t-tsyn\t F\t D1\t D2\t amp\t newF\t newD1\t newD2\n")
}

        F = 1 + (F-1)*exp(-(t - tsyn)/tau_F)
        D1 = 1 - (1-D1)*exp(-(t - tsyn)/tau_D1)
        D2 = 1 - (1-D2)*exp(-(t - tsyn)/tau_D2)
: printf("%g\t%g\t%g\t%g\t%g\t%g", t, t-tsyn, F, D1, D2, weight*F*D1*D2)
        tsyn = t

	state_discontinuity(A, A + weight*factor*F*D1*D2)    : assigns A=A+... once per timestep
	state_discontinuity(B, B + weight*factor*F*D1*D2)
	total = total+weight*F*D1*D2

        F = F + f
        D1 = D1 * d1
        D2 = D2 * d2
: printf("\t%g\t%g\t%g\n", F, D1, D2)


: NET_RECEIVE(w (uS)) {LOCAL ww
:   ww=w
:   A = A + ww*factor
:   B = B + ww*factor
: }











