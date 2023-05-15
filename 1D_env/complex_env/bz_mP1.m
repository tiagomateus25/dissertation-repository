function bz_mP1=bz_mP1(p,z,mP1,z1)

bz_mP1=0;
for i=1:2
bz_mP1=bz_mP1+((-1)^i)*bz(p,z,mP1(i,:),z1);
end

end