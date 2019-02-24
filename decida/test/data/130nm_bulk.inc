*
* Predictive Technology Model Beta Version
* 130nm NMOS SPICE Parametersv (normal one)
*

.model NMOS NMOS
+Level = 49

+Lint = 2.5e-08 Tox = 3.3e-09 
+Vth0 = 0.332 Rdsw = 200 

+lmin=1.3e-7 lmax=1.3e-7 wmin=1.3e-7 wmax=1.0e-4 Tref=27.0 version =3.1
+Xj= 4.5000000E-08          Nch= 5.6000000E+17 
+lln= 1.0000000            lwn= 0.00                  wln= 0.00
+wwn= 1.0000000            ll= 0.00
+lw= 0.00                  lwl= 0.00                  wint= 0.00
+wl= 0.00                  ww= 0.00                   wwl= 0.00
+Mobmod= 1                 binunit= 2                 xl= 0
+xw= 0                     binflag=  0
+Dwg= 0.00                 Dwb= 0.00 

+K1= 0.3661500              K2= 0.00 
+K3= 0.00                  Dvt0= 8.7500000            Dvt1= 0.7000000 
+Dvt2= 5.0000000E-02       Dvt0w= 0.00                Dvt1w= 0.00 
+Dvt2w= 0.00               Nlx= 3.5500000E-07         W0= 0.00 
+K3b= 0.00                 Ngate= 5.0000000E+20 

+Vsat= 1.3500000E+05       Ua= -1.8000000E-09         Ub= 2.2000000E-18 
+Uc= -2.9999999E-11        Prwb= 0.00 
+Prwg= 0.00                Wr= 1.0000000              U0= 1.3400000E-02 
+A0= 2.1199999             Keta= 4.0000000E-02        A1= 0.00 
+A2= 0.9900000             Ags= -0.1000000            B0= 0.00 
+B1= 0.00 

+Voff= -7.9800000E-02      NFactor= 1.1000000         Cit= 0.00 
+Cdsc= 0.00                Cdscb= 0.00                Cdscd= 0.00 
+Eta0= 4.0000000E-02       Etab= 0.00                 Dsub= 0.5200000 

+Pclm= 0.1000000           Pdiblc1= 1.2000000E-02     Pdiblc2= 7.5000000E-03 
+Pdiblcb= -1.3500000E-02   Drout= 0.2800000           Pscbe1= 8.6600000E+08 
+Pscbe2= 1.0000000E-20     Pvag= -0.2800000           Delta= 1.0100000E-02 
+Alpha0= 0.00              Beta0= 30.0000000 

+kt1= -0.3400000           kt2= -5.2700000E-02        At= 0.00 
+Ute= -1.2300000           Ua1= -8.6300000E-10        Ub1= 2.0000001E-18 
+Uc1= 0.00                 Kt1l= 4.0000000E-09        Prt= 0.00 

+Cj= 0.0015                Mj= 0.7175511              Pb= 1.24859
+Cjsw= 2E-10               Mjsw= 0.3706993            Php= 0.7731149
+Cta= 9.290391E-04         Ctp= 7.456211E-04          Pta= 1.527748E-03
+Ptp= 1.56325E-03          JS=2.50E-08                JSW=4.00E-13
+N=1.0                     Xti=3.0                    Cgdo=2.75E-10
+Cgso=2.75E-10             Cgbo=0.0E+00               Capmod= 2
+NQSMOD= 0                 Elm= 5                     Xpart= 1
+Cgsl= 1.1155E-10          Cgdl= 1.1155E-10           Ckappa= 0.8912
+Cf= 1.113e-10             Clc= 5.475E-08             Cle= 6.46
+Dlc= 2E-08                Dwc= 0                     Vfbcv= -1

*
* Predictive Technology Model Beta Version
* 130nm PMOS SPICE Parametersv (normal one)
*

.model PMOS PMOS
+Level = 49

+Lint = 2.e-08 Tox = 3.3e-09 
+Vth0 = -0.3499 Rdsw = 400 

+lmin=1.3e-7 lmax=1.3e-7 wmin=1.3e-7 wmax=1.0e-4 Tref=27.0 version =3.1
+Xj= 4.5000000E-08         Nch= 6.8500000E+18 
+lln= 0.00                 lwn= 0.00                  wln= 0.00
+wwn= 0.00                 ll= 0.00
+lw= 0.00                  lwl= 0.00                  wint= 0.00
+wl= 0.00                  ww= 0.00                   wwl= 0.00
+Mobmod=  1                binunit= 2                 xl=  0
+xw=  0                    binflag=  0
+Dwg= 0.00                 Dwb= 0.00 

+K1= 0.4087000             K2= 0.00 
+K3= 0.00                  Dvt0= 5.0000000            Dvt1= 0.2600000 
+Dvt2= -1.0000000E-02      Dvt0w= 0.00                Dvt1w= 0.00 
+Dvt2w= 0.00               Nlx= 1.6500000E-07         W0= 0.00 
+K3b= 0.00                 Ngate= 5.0000000E+20 

+Vsat= 1.0500000E+05       Ua= -1.4000000E-09         Ub= 1.9499999E-18 
+Uc= -2.9999999E-11        Prwb= 0.00 
+Prwg= 0.00                Wr= 1.0000000              U0= 5.2000000E-03 
+A0= 2.1199999             Keta= 3.0300001E-02        A1= 0.00 
+A2= 0.4000000             Ags= 0.1000000             B0= 0.00 
+B1= 0.00 

+Voff= -9.10000000E-02     NFactor= 0.1250000         Cit= 2.7999999E-03 
+Cdsc= 0.00                Cdscb= 0.00                Cdscd= 0.00 
+Eta0= 80.0000000          Etab= 0.00                 Dsub= 1.8500000 

+Pclm= 2.5000000           Pdiblc1= 4.8000000E-02     Pdiblc2= 5.0000000E-05 
+Pdiblcb= 0.1432509        Drout= 9.0000000E-02       Pscbe1= 1.0000000E-20 
+Pscbe2= 1.0000000E-20     Pvag= -6.0000000E-02       Delta= 1.0100000E-02 
+Alpha0= 0.00              Beta0= 30.0000000 

+kt1= -0.3400000           kt2= -5.2700000E-02        At= 0.00 
+Ute= -1.2300000           Ua1= -8.6300000E-10        Ub1= 2.0000001E-18 
+Uc1= 0.00                 Kt1l= 4.0000000E-09        Prt= 0.00 

+Cj= 0.0015                Mj= 0.7175511              Pb= 1.24859
+Cjsw= 2E-10               Mjsw= 0.3706993            Php= 0.7731149
+Cta= 9.290391E-04         Ctp= 7.456211E-04          Pta= 1.527748E-03
+Ptp= 1.56325E-03          JS=2.50E-08               JSW=4.00E-13
+N=1.0                     Xti=3.0                   Cgdo=2.75E-10
+Cgso=2.75E-10             Cgbo=0.0E+00              Capmod= 2
+NQSMOD= 0                 Elm= 5                    Xpart= 1
+Cgsl= 1.1155E-10          Cgdl= 1.1155E-10          Ckappa= 0.8912
+Cf= 1.113e-10             Clc= 5.475E-08            Cle= 6.46
+Dlc= 2E-08                Dwc= 0                    Vfbcv= -1

