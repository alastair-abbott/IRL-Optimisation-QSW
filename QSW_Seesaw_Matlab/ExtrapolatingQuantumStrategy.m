c24 = stateCoeffs(:,1)-(stateCoeffs(:,2)-stateCoeffs(:,1))*2;
normcoeff24 = sqrt(1/3*(1-(c24(1)^2 + 3*c24(2)^2 + c24(4)^2)));
psi24 = [c24(1); c24(2); c24(2); -normcoeff24; c24(2); -normcoeff24; -normcoeff24; -c24(4)];
rho24 = psi24*psi24';

c22 = stateCoeffs(:,1)-(stateCoeffs(:,2)-stateCoeffs(:,1))*4;
normcoeff22 = sqrt(1/3*(1-(c22(1)^2 + 3*c22(2)^2 + c22(4)^2)));
psi22 = [c22(1); c22(2); c22(2); -normcoeff22; c22(2); -normcoeff22; -normcoeff22; -c22(4)];
rho22 = psi22*psi22';

c20 = stateCoeffs(:,1)-(stateCoeffs(:,2)-stateCoeffs(:,1))*6;
normcoeff20 = sqrt(1/3*(1-(c20(1)^2 + 3*c20(2)^2 + c20(4)^2)));
psi20 = [c20(1); c20(2); c20(2); -normcoeff20; c20(2); -normcoeff20; -normcoeff20; -c20(4)];
rho20 = psi20*psi20';

m24 = measurementParam(1) - (measurementParam(2)-measurementParam(1))*2;
m22 = measurementParam(1) - (measurementParam(2)-measurementParam(1))*4;
m20 = measurementParam(1) - (measurementParam(2)-measurementParam(1))*6;

v24 = [cos(m24/2); sin(m24/2)];
v22 = [cos(m22/2); sin(m22/2)];
v20 = [cos(m20/2); sin(m20/2)];

M24 = cell(1,3);
M22 = cell(1,3);
M20 = cell(1,3);

for k = 1:3
   M24{k} = zeros(2,2,2,2); 
   
   M24{k}(:,:,1,1) = [1,0;0,0];
   M24{k}(:,:,2,1) = [0,0;0,1];
   
   M22{k} = M24{k};
   M20{k} = M24{k};
   
   M24{k}(:,:,1,2) = v24*v24';
   M24{k}(:,:,2,2) = eye(2) - v24*v24';
   
   M22{k}(:,:,1,2) = v22*v22';
   M22{k}(:,:,2,2) = eye(2) - v22*v22';
   
   M20{k}(:,:,1,2) = v20*v20';
   M20{k}(:,:,2,2) = eye(2) - v20*v20';
end

