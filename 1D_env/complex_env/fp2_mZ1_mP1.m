function fp2_mZ1_mP1=fp2_mZ1_mP1(p,z,mP1,mZ1,t1)

fp2_mZ1_mP1=0;
for i=1:2
    for j=1:2
        fp2_mZ1_mP1=fp2_mZ1_mP1+((-1)^(i+j))*fp2(p,z,mP1(i,:),mZ1(j,:),t1);
    end
end

end