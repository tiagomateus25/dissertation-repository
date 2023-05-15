function fp_mP1=fp_mP1(p,z,mP1,z1)

fp_mP1=0;
for i=1:2
fp_mP1=fp_mP1+((-1)^i)*fp(p,z,mP1(i,:),z1);
end

end