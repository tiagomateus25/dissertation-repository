function [A01,A0d1,A0V1,A021,A0dddt1,A0n1] = function12(ind1,Res2,t,I,d0,nt,nk,f2,SampleRate,n,n1,Plength,Xcm,a0Out,Rc,Lc,mMassi,opts,g_acel,movTFz,movtFz,Fg_m,Dampf,Dampc_m,Dampf1);


Res=Res2(ind1);
% V=I*Res;                      % Voltage of the external circuit in V as fuction of current (I)
% Vcircuit=matlabFunction(V,'vars',{'t','I'});
y0=[d0,0,0];

V=I*Res;
Vcircuit=matlabFunction(V,'vars',{'t','I'}); 

t_1=zeros(nt+1,nk);y_1=zeros(nt+1,4,nk); Pow=zeros(nt+1,nk); AvPow=zeros(1,nk); mFzi=zeros(nt+1,nk); iFzi=mFzi; Ffic_m=Pow; FficVel_m=Pow; AFfic_m=AvPow; AvFficVel_m=AvPow; 
f_1=zeros(floor(nt/2),nk); Y_1=zeros(floor(nt/2),4,nk); Yf_1=zeros(4,nk); Yf_2=Yf_1; Yf_3=Yf_1; Y_max=Yf_1; f_max=Yf_1;
tic
for k=1:nk
% k
ff2=f2(k);                 % Input frequency
dt=1/(SampleRate*ff2);     % dt = 1/(SampleRate*f1); tfinal = (nt-1)*dt ~ Ncicles/ff
df=1/(nt*dt);             % df = 1/(nt*dt) ~ f1/Ncicles; ffinal = (nt-1)/(nt*dt) ~ 1/dt = SampleRate*ff

t0=n1*dt;                  
f1=n*df;                  
ww=2*pi*ff2;

%%% Numerical calculations Options %%%%%%%% 

% % Complete ODE %
% [t1,y] = ode15s(@(t,y) [y(2); movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+((mFzif(mM,mP1,mZ11,mL,i,J,y(1),AbsTol,RelTol,u0)+y(3)*alphaEMf(iP,iZ,mM,mP1,mL,i,y(1),Ncoil,u0,cI))/mMassi)+Ffric_mf(y(2),Dampf,Dampc_m,Dampf1,movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+((mFzif(mM,mP1,mZ11,mL,i,J,y(1),AbsTol,RelTol,u0)+y(3)*alphaEMf(iP,iZ,mM,mP1,mL,i,y(1),Ncoil,u0,cI))/mMassi));(Vcircuit(t,y(3))+Rc*y(3)+(alphaEMf(iP,iZ,mM,mP1,mL,i,y(1),Ncoil,u0,cI))*y(2))/(-Lc)], t0, y0, opts);
% y_1(:,4,k)=Vcircuit(t1,y(:,3)); % Output Voltage vs time
% 
% % Open-circuit conditions (I = 0) %
% [t1,y] = ode45(@(t,y) [y(2); movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+((mFzif(mM,mP1,mZ11,mL,i,J,y(1),AbsTol,RelTol,u0))/mMassi)+Ffric_mf(y(2),Dampf,Dampc_m,Dampf1,movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+((mFzif(mM,mP1,mZ11,mL,i,J,y(1),AbsTol,RelTol,u0))/mMassi))], t0, y0(1:2), opts);
% y(:,3)=0;
% y_1(:,4,k)=-y(:,2).*alphaEMf(iP,iZ,mM,mP1,mL,i,y(:,1).',Ncoil,u0,cI); % Output Voltage vs time
% 
% % Low frequency approximation (wL << R) %
% [t1,y] = ode45(@(t,y) [y(2); movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+((mFzif(mM,mP1,mZ11,mL,i,J,y(1),AbsTol,RelTol,u0)-y(2)*((alphaEMf(iP,iZ,mM,mP1,mL,i,y(1).',Ncoil,u0,cI).^2)./(Res+Rc)))/mMassi)+Ffric_mf(y(2),Dampf,Dampc_m,Dampf1,movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+(mFzif(mM,mP1,mZ11,mL,i,J,y(1),AbsTol,RelTol,u0)/mMassi))], t0, y0(1:2), opts);
% y(:,3)=-y(:,2).*(alphaEMf(iP,iZ,mM,mP1,mL,i,y(:,1).',Ncoil,u0,cI)./(Res+Rc));
% y_1(:,4,k)=Res*y(:,3);
% 
% % Complete ODE (Interpolate a0Out.mat from Magnetics.m) %
% [t1,y] = ode15s(@(t,y) [y(2); movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+((interp1(a0Out(:,1),a0Out(:,2),y(1),'spline')+y(3)*interp1(a0Out(:,1),a0Out(:,3),y(1),'spline'))/mMassi)+Ffric_mf(y(2),Dampf,Dampc_m,Dampf1,movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+((interp1(a0Out(:,1),a0Out(:,2),y(1),'spline')+y(3)*interp1(a0Out(:,1),a0Out(:,3),y(1),'spline'))/mMassi));(Vcircuit(t,y(3))+Rc*y(3)+(interp1(a0Out(:,1),a0Out(:,3),y(1),'spline'))*y(2))/(-Lc)], t0, y0, opts);
% y_1(:,4,k)=Vcircuit(t1,y(:,3)); % Output Voltage vs time

% Low frequency approximation (wL << R) (Interpolate a0Out.mat from Magnetics.m) %
[t1,y] = ode45(@(t,y) [y(2); movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+Fmag_m_int(y,a0Out,mMassi)+Flrz_m_int(y,a0Out,mMassi,Res,Rc)+Ffric_mf(y(2),Dampf,Dampc_m,Dampf1,movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+Fmag_m_int(y,a0Out,mMassi)+Flrz_m_int(y,a0Out,mMassi,Res,Rc))], t0, y0(1:2), opts);
y(:,3)=-y(:,2).*(interp1(a0Out(:,1),a0Out(:,3),y(:,1),'linear','extrap')./(Res+Rc));
y_1(:,4,k)=Res*y(:,3);

% % Parallel connection - Low frequency approximation (wL << R) (Interpolate a0Out.mat from Magnetics.m) %
% [t1,y] = ode45(@(t,y) [y(2); movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+Fmag_m_int(y,a0Out,mMassi)+Flrz_m_int_P(y,a0Out,Flrz_v,mMassi,Res,Rc)+Ffric_mf(y(2),Dampf,Dampc_m,Dampf1,movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+Fmag_m_int(y,a0Out,mMassi)+Flrz_m_int_P(y,a0Out,Flrz_v,mMassi,Res,Rc))], t0, y0(1:2), opts);
% y(:,3)=-y(:,2).*(interp1(a0Out(:,1),I_v.',y(:,1),'spline'));
% y_1(:,4,k)=Res*y(:,3);

t_1(:,k)=t1;            % Time
y_1(:,1:3,k)=y;           % Output [delta, ddelta/dt, I, V] vs time
Pow(:,k)=y_1(:,3,k).*y_1(:,4,k); % Output power vs time (I*V)
AvPow(k)=(sum(Pow(:,k))-(1/2)*(Pow(1,k)+Pow(end,k)))/nt; % Output average power 

Ffic_m(:,k)=movTFz(t_1(:,k),ww)+(y_1(:,1,k)+Plength+Xcm)*movtFz(t_1(:,k),ww);  % Fictitious_force/mass
AFfic_m(k)=max(abs(Ffic_m(:,k))); % Fictitious_force/mass max amplitude
% Ftotal_m(:,k)=Ffic_m(:,k)+Fg_m(t1,ww)+Fmag_m_int(y.',a0Out,mMassi).'+Flrz_m_int(y.',a0Out,mMassi,Res,Rc).'+Ffric_mf(y(:,2),Dampf,Dampc_m,Dampf1,Ffic_m(:,k)+Fg_m(t1,ww)+Fmag_m_int(y.',a0Out,mMassi).'+Flrz_m_int(y.',a0Out,mMassi,Res,Rc).');
Ftotal_m(:,k)=Flrz_m_int(y.',a0Out,mMassi,Res,Rc).'+Ffric_mf(y(:,2),Dampf,Dampc_m,Dampf1,Ffic_m(:,k)+Fg_m(t1,ww)+Fmag_m_int(y.',a0Out,mMassi).'+Flrz_m_int(y.',a0Out,mMassi,Res,Rc).');
% Ftotal_m(:,k)=gradient(y(:,2))/dt;
Ftotal_Vel_m(:,k)=Ftotal_m(:,k).*y(:,2);
AvFtotalVel_m(k)=(sum(Ftotal_Vel_m(:,k))-(1/2)*(Ftotal_Vel_m(1,k)+Ftotal_Vel_m(end,k)))/nt;
% FficVel_m(:,k)=Ffic_m(:,k).*y_1(:,2,k); % Fictitious_force.free_magnet_velocity/mass
% AvFficVel_m(k)=(sum(FficVel_m(:,k))-(1/2)*(FficVel_m(1,k)+FficVel_m(end,k)))/nt; % Average Fictitious_force.free_magnet_velocity/mass

%%% DFT
% Y=fft(y_1(1:end-1,:,k)); % FFT
% 
% f_1(:,k)=f1(1:end/2);   % Ouput frequency
% Y_1(:,:,k)=2*Y(1:end/2,:)/nt;  %(DFT [Displacement; Velocity; Current; Voltage])
% 
% Inter=-2:2;
% Yf_1(:,k)=max(interp1(f_1(:,k),Y_1(:,:,k),ff2+df*Inter,'linear')).';    % Interpolation of DFT at f_i_n (DFT [Displacement; Velocity; Current; Voltage])
%%% Peak


Yf_1(:,k)=max(abs(y_1(:,:,k)));
%%%


% Yf_2(:,k)=max(interp1(f_1(:,k),Y_1(:,:,k),2*ff2+df*Inter,'linear')).';  % 2.f_i_n
% Yf_3(:,k)=max(interp1(f_1(:,k),Y_1(:,:,k),3*ff2+df*Inter,'linear')).';  % 3.f_i_n

% [~,i_1max1]=max(abs(Y_1(2:end,:,k)));    % Max of DFT
% Y_1max1=Y_1(i_1max1+1,:,k);
% Y_max(:,k)=diag(Y_1max1);
% f_max(:,k)=f_1(i_1max1+1,k);

% for l=1:nt  % Forces vs time calculations
% mFzi(l,k)=mFzif(mM,mP1,mZ11,mL,i,J,y(l,1),AbsTol,RelTol,u0);       % Lorentz force by magnets on free magnet
% iFzi(l,k)=y(l,3)*(dObijf(iP,iZ,mM,mP1,mZ11,mL,i,y(l,1),Ncoil,u0)*cI.');  % Lorentz force by coils on free magnet
% end

y0 = y(end,:);

end
toc

AvPow_a2=AvPow./((AFfic_m/g_acel).^2);       % Average output power / free magnet acceleration^2 (W/g^2)
AvPow_AvPowIn=100*AvPow./(mMassi.*abs(AvFtotalVel_m));  % Average output power / Average free magnet (%)
% V_a=abs(Yf_1(4,:))./((AFfic_m/g_acel).^1);    % Voltage / free magnet acceleration (V/g)

A01=AvPow.';
A0d1=abs(Yf_1(1,:)).';
A0V1=abs(Yf_1(4,:)).';
A021=AvPow_a2.';
A0dddt1=abs(Yf_1(2,:)).'; %velocity;
A0n1=AvPow_AvPowIn;
end
