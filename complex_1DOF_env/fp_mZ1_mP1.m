function fp_mZ1_mP1=fp_mZ1_mP1(p,z,mP1,mZ1)

fp_mZ1_mP1=0;
for i=1:2
    for j=1:2
        fp_mZ1_mP1=fp_mZ1_mP1+((-1)^(i+j))*fp(p,z,mP1(i,:),mZ1(j,:));
    end
end

end