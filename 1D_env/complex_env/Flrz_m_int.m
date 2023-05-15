function Flrz_m=Flrz_m_int(y,a0Out,mMassi,Res,Rc)
alphaEM=interp1(a0Out(:,1),a0Out(:,3),y(1,:),'linear','extrap');
Flrz_m=-((alphaEM.^2)./((Res+Rc).*mMassi)).*y(2,:);
end