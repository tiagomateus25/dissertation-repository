function Ffric_m = Ffric_mf(v,Dampf,Dampc_m,Dampf1,Fin_m)  % Friction force/mass in N/kg
if abs(v)<=1e-16
    if abs(Fin_m)<Dampf1
        Ffric_m=-Fin_m;
    else
        Ffric_m=-Dampf1*sign(Fin_m);
    end
else
    Ffric_m=-(Dampf*sign(v)+Dampc_m*v);
end
end