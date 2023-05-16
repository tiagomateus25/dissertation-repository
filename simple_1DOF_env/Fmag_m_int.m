function Fmag_m=Fmag_m_int(y,a0Out,mMassi)
Fmag_m=interp1(a0Out(:,1),a0Out(:,2),y(1,:),'linear','extrap')./mMassi;
end