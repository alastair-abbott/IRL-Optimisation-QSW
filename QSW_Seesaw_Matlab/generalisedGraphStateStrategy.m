function [rho,M] = generalisedGraphStateStrategy(n,theta)
%generalisedGraphStateStrategy Returns state and measurements for generalised Graph state strategy
%   [rho,M] = generalisedGraphStateStrategy(n,theta)
%   n: number of parties
%   theta: parameter of deviated strategies. theta = pi/2 by default (standard graph state)
    arguments
       n {mustBeMember(n,[3,5])} = 3;
       theta (1,1) double = pi/2;
    end
    
    d = 2;
    
    psi_theta = [cos(theta/2); sin(theta/2)];
    phi_theta = [sin(theta/2); -cos(theta/2)];
    
    CZ12 = eye(4);
    CZ12(4,4) = -1;
    CZ12 = Tensor(CZ12, eye(2^(n-2))); % CZ between first 2 systems, id on rest

    CZ = cell(1,n);
    CZ{1} = CZ12;
    for i = 2:n
        CZ{i} = PermuteSystems(CZ12, [(n-i+2):n, 1:(n-i+1)], 2*ones(1,n));
    end

    psi_G = Tensor(psi_theta, n);
    for k = 1:n
       psi_G = CZ{k}*psi_G; 
    end
    rho = psi_G*psi_G';

    M = cell(1,n);

    for k = 1:n
        Mk = zeros(d,d,2,2);
        Mk(:,:,1,1) = [1,0;0,0];
        Mk(:,:,2,1) = [0,0;0,1];
        Mk(:,:,1,2) = psi_theta*psi_theta';
        Mk(:,:,2,2) = phi_theta*phi_theta';
        M{k} = Mk;
    end

end

