n = 5;
sym = false;
[rho,M] = generalisedGraphStateStrategy(n);
i = 1;
v0 = 1.33:0.005:1.34;
equilQ = zeros(1,length(v0));
equilQcorr = zeros(1,length(v0));
for i = 1:length(v0)
   game = CycleGame(n,[v0(i), 2-v0(i)], sym); 
   equilQ(i) = isQuantumEquilibrium(game,rho,M,1e-6);
   equilQcorr(i) = isQuantumCorrelatedEquilibrium(game,rho,M,1e-6);
end

[v0; equilQ; equilQcorr]