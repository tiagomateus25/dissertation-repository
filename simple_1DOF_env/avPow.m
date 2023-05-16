function AvPow = avPow(State, Action)

load('a0Out_40_2C.mat')
load('a0Out_40_4C.mat')

% Define the environment constants.
syms t w                                                 % Time (t) and angular frequency (w)  symbolic variables

Rc_2C=8.41e+03;
Rc_4C=2*Rc_2C;                                           % Effective resistance of the coils in Ohm

Res_array = [150000,50000,5000, 500]; %%%%%%%%%%%%try only 5 res

nf=101;                                                  % Number of frequency sweep points
fi=1;                                                    % Initial frequency in Hz
ff=6;                                                    % Final  frequency in Hz
% nf2=1001;

Amplitude=(20E-3)*(w^2);                                 % sym(10) % Acceleration Amplitude in m/s^2 (parameter in analytical solution with forcing term -d2Tdt2=Amplitude*cos(w*t)) (e.g. =sym(10), constant acceleration; =(1E-3)*(w^2), constant displacement)
T3=Amplitude*(1/(w^2))*cos(w*t);                         % Translation vector components in m as functions of time (t) (e.g. Amplitude*(1/(w^2))*cos(w*t), acceleration = -A.cos(w.t))
T2=sym(0);
T1=sym(0);

AmplitudeAlpha=sqrt(0);                                  % Amplitude in rad/s (parameter in analytical solution with forcing term (delta+Plength+Xcm)*(sin(beta0)^2)*(dalphadt^2)=(delta+Plength+Xcm)*(sin(beta0)^2)*((AmplitudeAlpha*cos((w/2)*t))^2)
alpha=AmplitudeAlpha*(1/((w/2)^1))*sin((w/2)*t);         % Rotational Euler angle components in radians as functions of time (t) (e.g. AmplitudeAlpha*(1/((w/2)^1))*sin((w/2)*t))
beta=0;                                                  % e.g. =0 V =pi/2 (no gravity pull)
Plength=0;                                               % Distance between pivot point and z=0 of cylinder in m (for rotational motions)
Xcm=0;  %(24.46-(1/2)*(6*3))*1e-3;                       % Center of mass of the free moving body in relation center of the free magnet in m 

Dampc=0.2;                    % c Drag constant in N/(m/s) (~0.25-0.4) (Drag force = -mass*Dampf*sign(v)-Dampc*v)1
Dampf=0.0;                    % f/m Friction force in N/kg (~ 0.4*|sin(beta)| for Teflon) (can make calculations very slow for low excitation amplitudes! => set to 0)
Dampf1=Dampf;                 % f/m Static friction force in N/kg  (~=Dampf for Teflon)

GravPull=0;                   % Gravity Force in ODE (0 - false; 1 - true)

y0 = [0,0,0];                 % Initial conditions [delta - position, ddelta/dt - velocity, I - current] (m, m/s, A)
SampleRate=200;               % Number of time points per cicle in ODE solution (defines maximum frequency in DFT)
Ncicles=5;                    % Number of time cycles in ODE solution (defines spacing between DFT points)
AbsTolOde=1e-6;               % Absolute error tolerance in ODE (default = 1e-6)
RelTolOde=1e-3;               % Relative error tolerance in ODE (default = 1e-3)

mMassi=20.1455*1e-3;         % 7.4e3*(2*mL(i)*pi*(mPo(i)^2-mPi(i)^2));%+8.49e-3;  % Mass of the i magnet in kg (+ guiding rod) 

g_acel=9.80665;              % Gravitational acceleration in m/s^2
Dampc_m=Dampc/mMassi;

% Calculations
f2=linspace(fi,ff,nf);

dT3dt2=diff(T3,t,2); dT2dt2=diff(T2,t,2); dT1dt2=diff(T1,t,2); 
movTFz=matlabFunction(-cos(beta)*dT3dt2+sin(beta)*cos(alpha)*dT2dt2-sin(beta)*sin(alpha)*dT1dt2,'vars',{'t','w'}); % Fictitious force due to translations/mass
dalphadt=diff(alpha,t,1); dbetadt=diff(beta,t,1); 
movtFz=matlabFunction((dbetadt.^2)+(dalphadt.^2).*(sin(beta).^2),'vars',{'t','w'}); % Fictitious force due to rotations/mass

if GravPull==1
    Fg_m=matlabFunction(sym(-g_acel*cos(beta)),'vars',{'t','w'}) ; % Gravity force/mass     
else
    Fg_m=@(t,w) 0;
end

% Time/Frequency response

nt=round(SampleRate * Ncicles);
n1=0:nt;         
nk=length(f2);
opts = odeset('RelTol',RelTolOde,'AbsTol',AbsTolOde);
y_1=zeros(nt+1,4,nk);

% Unpack the state vector from the logged signals.

State = double(State);
ff2 = State(1);    % Input frequency

dt=1/(SampleRate*ff2);                                                         % dt = 1/(SampleRate*f1); tfinal = (nt-1)*dt ~ Ncicles/ff
t0=n1*dt;                                   
ww=2*pi*ff2;

% Check if the given action is valid.
if ~ismember(Action,1:8)
    error('Action does not exist within array');
end

index_pos_2C = find((1:4)==Action);
index_pos_4C = find((5:8)==Action);
if index_pos_2C
    a0Out = a0Out_40_2C;
    Rc = Rc_2C;
    Res = Res_array(index_pos_2C);
elseif index_pos_4C
    a0Out = a0Out_40_4C;
    Rc = Rc_4C;
    Res = Res_array(index_pos_4C);
end

% Low frequency approximation (wL << R) (Interpolate a0Out.mat from Magnetics.m).
[t1,y] = ode45(@(t,y) [y(2); movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+Fmag_m_int(y,a0Out,mMassi)+Flrz_m_int(y,a0Out,mMassi,Res,Rc)+Ffric_mf(y(2),Dampf,Dampc_m,Dampf1,movTFz(t,ww)+(y(1)+Plength+Xcm)*movtFz(t,ww)+Fg_m(t,ww)+Fmag_m_int(y,a0Out,mMassi)+Flrz_m_int(y,a0Out,mMassi,Res,Rc))], t0, y0(1:2), opts);
y(:,3)=-y(:,2).*(interp1(a0Out(:,1),a0Out(:,3),y(:,1),'linear','extrap')./(Res+Rc));
y_1(:,4)=Res*y(:,3);

t_1 = t1;                                                                    % Time
y_1(:,1:3)=y;                                                                % Output [delta, ddelta/dt, I, V] vs time
Pow=y_1(:,3).*y_1(:,4);                                                      % Output power vs time (I*V)
AvPow=(sum(Pow)-(1/2)*(Pow(1)+Pow(end)))/nt;                                 % Output average power

% new_freq = ff2 + 1;
% total_AvPow = Init_AvPow + AvPow;

% if new_freq == 6
%     % Perform Euler integration.
%     LoggedSignals.State = [1; 0; total_AvPow];
% 
%     % Transform state to observation.
%     NextObs = LoggedSignals.State;
% 
%     % Check terminal condition.
%     IsDone = NextObs(3) < Init_total_AvPow;
% 
%     if ~IsDone
%         % Get reward
%         Reward = 1;
%     else
%         % Get reward
%         Reward = -10;
%     end
% 
% else
%     % Perform Euler integration.
%     LoggedSignals.State = [new_freq; total_AvPow; Init_total_AvPow];
% 
%     % Transform state to observation.
%     NextObs = LoggedSignals.State;
% 
%     % Check terminal condition.
%     IsDone = false;
% 
%     % Get reward
%     Reward = 0;
% end

end