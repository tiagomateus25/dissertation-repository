function Flrz_m=Flrz_m_int_P(y,a0Out,Flrz_v,mMassi,Res,Rc)
alphaEM2=interp1(a0Out(:,1),Flrz_v,y(1),'linear','extrap');
Flrz_m=-(alphaEM2/mMassi)*y(2);
end