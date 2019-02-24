*==============================================================================
* Predictive Technology Model Beta Version
* 130nm NMOS SPICE Parameters (normal one)
*==============================================================================
.model nmos nmos level=49
+ lint=2.5e-08              tox=__tox_n               vth0=__vth0_n            
+ lmin=1.3e-7               lmax=1.3e-7               wmin=1.3e-7              
+ tref=27.0                 version=3.1               xj=4.5000000e-08         
+ lln=1.0000000             lwn=0.00                  wln=0.00                 
+ ll=0.00                   lw=0.00                   lwl=0.00                 
+ wl=0.00                   ww=0.00                   wwl=0.00                 
+ binunit=2                 xl=__xl_n                 xw=__xw_n                
+ dwg=0.00                  dwb=0.00                  k1=0.3661500             
+ k3=0.00                   dvt0=8.7500000            dvt1=0.7000000           
+ dvt0w=0.00                dvt1w=0.00                dvt2w=0.00               
+ w0=0.00                   k3b=0.00                  ngate=5.0000000e+20      
+ ua=-1.8000000e-09         ub=2.2000000e-18          uc=-2.9999999e-11        
+ prwg=0.00                 wr=1.0000000              u0=__u0_n
+ keta=4.0000000e-02        a1=0.00                   a2=0.9900000             
+ b0=0.00                   b1=0.00                   voff=-7.9800000e-02      
+ cit=0.00                  cdsc=0.00                 cdscb=0.00               
+ eta0=4.0000000e-02        etab=0.00                 dsub=0.5200000           
+ pdiblc1=1.2000000e-02     pdiblc2=7.5000000e-03     pdiblcb=-1.3500000e-02   
+ pscbe1=8.6600000e+08      pscbe2=1.0000000e-20      pvag=-0.2800000          
+ alpha0=0.00               beta0=30.0000000          kt1=-0.3400000           
+ at=0.00                   ute=-1.2300000            ua1=-8.6300000e-10       
+ uc1=0.00                  kt1l=4.0000000e-09        prt=0.00                 
+ mj=0.7175511              pb=1.24859                cjsw=2e-10               
+ php=0.7731149             cta=9.290391e-04          ctp=7.456211e-04         
+ ptp=1.56325e-03           js=2.50e-08               jsw=4.00e-13             
+ xti=3.0                   cgdo=2.75e-10             cgso=2.75e-10            
+ capmod=2                  nqsmod=0                  elm=5                    
+ cgsl=1.1155e-10           cgdl=1.1155e-10           ckappa=0.8912            
+ clc=5.475e-08             cle=6.46                  dlc=2e-08                
+ vfbcv=-1                 
.model pmos pmos level=49
+ lint=2.e-08               tox=__tox_p               vth0=__vth0_p            
+ lmin=1.3e-7               lmax=1.3e-7               wmin=1.3e-7              
+ tref=27.0                 version=3.1               xj=4.5000000e-08         
+ lln=0.00                  lwn=0.00                  wln=0.00                 
+ ll=0.00                   lw=0.00                   lwl=0.00                 
+ wl=0.00                   ww=0.00                   wwl=0.00                 
+ binunit=2                 xl=__xl_p                 xw=__xw_p                
+ dwg=0.00                  dwb=0.00                  k1=0.4087000             
+ k3=0.00                   dvt0=5.0000000            dvt1=0.2600000           
+ dvt0w=0.00                dvt1w=0.00                dvt2w=0.00               
+ w0=0.00                   k3b=0.00                  ngate=5.0000000e+20      
+ ua=-1.4000000e-09         ub=1.9499999e-18          uc=-2.9999999e-11        
+ prwg=0.00                 wr=1.0000000              u0=__u0_p
+ keta=3.0300001e-02        a1=0.00                   a2=0.4000000             
+ b0=0.00                   b1=0.00                   voff=-9.10000000e-02     
+ cit=2.7999999e-03         cdsc=0.00                 cdscb=0.00               
+ eta0=80.0000000           etab=0.00                 dsub=1.8500000           
+ pdiblc1=4.8000000e-02     pdiblc2=5.0000000e-05     pdiblcb=0.1432509        
+ pscbe1=1.0000000e-20      pscbe2=1.0000000e-20      pvag=-6.0000000e-02      
+ alpha0=0.00               beta0=30.0000000          kt1=-0.3400000           
+ at=0.00                   ute=-1.2300000            ua1=-8.6300000e-10       
+ uc1=0.00                  kt1l=4.0000000e-09        prt=0.00                 
+ mj=0.7175511              pb=1.24859                cjsw=2e-10               
+ php=0.7731149             cta=9.290391e-04          ctp=7.456211e-04         
+ ptp=1.56325e-03           js=2.50e-08               jsw=4.00e-13             
+ xti=3.0                   cgdo=2.75e-10             cgso=2.75e-10            
+ capmod=2                  nqsmod=0                  elm=5                    
+ cgsl=1.1155e-10           cgdl=1.1155e-10           ckappa=0.8912            
+ clc=5.475e-08             cle=6.46                  dlc=2e-08                
+ vfbcv=-1                 
