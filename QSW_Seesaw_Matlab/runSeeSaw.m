n = 3;
sym = false;
d = 2;
yalmipOptions = sdpsettings('verbose',0,'solver','mosek','cachesolvers',1);

stepsize = 0.01;
numitersPerV0 = 1;

v0 = 0:stepsize:0.3;
% v0 = 0.2;
v1 = 2 - v0;
ratio = v0./v1;

numPoints = length(v0);

QSW = zeros(1,numPoints);
PWin = zeros(1,numPoints);
bestRho = zeros(d^n,d^n,numPoints);
bestM = cell(1,numPoints);

for i = 1:numPoints
    game = CycleGame(n,[v0(i), v1(i)], sym);
    for j = 1:numitersPerV0
        disp(['================= Starting iteration #', num2str(i), '.', num2str(j), '/', num2str(numPoints), ', v0/(v0+v1) = ', num2str(v0(i)/(v0(i)+v1(i))), ' ================='])
        
        initPOVMs = cell(1,game.n);
        for k = 1:game.n
            M = zeros(d,d,2,2);
            if d == 2
                % Fix first measurement to be a Z-basis measurement
                M(:,:,1,1) = [1,0;0,0];
                M(:,:,2,1) = [0,0;0,1];
            else
                M_t = RandomPVM(d,2);
                M(:,:,1,1) = M_t{1};
                M(:,:,2,1) = M_t{2};
            end
            
            for t = 2:2
%                 M_t = RandomPVM(d,2);
%                 M(:,:,1,t) = M_t{1};
%                 M(:,:,2,t) = M_t{2};
                M(:,:,1,t) = 1/2*[1,1;1,1];
                M(:,:,2,t) = 1/2*[1,-1;-1,1];
%                 M(:,:,1,t) = [1,0;0,0];
%                 M(:,:,2,t) = [0,0;0,1];
            end
            initPOVMs{k} = M;
        end

        [optQSW, optPWin, optRho, optPOVMs] = maxQswSeeSaw(game,d,[],initPOVMs,yalmipOptions);
        
        if optQSW > QSW(i)
            QSW(i) = optQSW;
            PWin(i) = optPWin;
            bestRho(:,:,i) = optRho;
            bestM{i} = optPOVMs;
            % Tidy things up
            bestRho(:,:,i) = Chop(bestRho(:,:,i));
            for k  = 1:game.n
               bestM{i}{k} = Chop(bestM{i}{k}); 
            end
        end
    end
    
end

%%
figure
plot(v0./(v0+v1),QSW,'x')

plotClassicalStrategies(n, sym)
plotNPABounds(n, sym);

grid on
hold off

%% Analyse the outpout
%close all

N = length(QSW);

if n == 3
    numStateCoeffs = 4;
else
    numStateCoeffs = 8;
end
stateCoeffs = zeros(numStateCoeffs,N);
measurementParam = zeros(1,N);

for i = flip(1:N)
    % Get the coefficients of the state
    [eigvecs,eigvals] = eig(bestRho(:,:,i),'vector');
    [~, ind] = sort(eigvals);
    bestPsi = eigvecs(:,ind(end)); % corresponds to max eigenval
    if n == 3
        stateCoeffs(:,i) = [-1;-1;1;1].*bestPsi([1,2,4,8]);
    elseif n == 5
        stateCoeffs(:,i) = [-1;-1;1;-1;-1;1;1;1].*bestPsi([1,2,4,6,8,12,16,32]);
    end
    stateCoeffs(:,i) = stateCoeffs(:,i)*sign(stateCoeffs(1,i));

    % Now get the meassurement parameter. Remember: all POVMs are the same now
    M10 = bestM{i}{1}(:,:,1,2);
    [eigvecs,eigvals] = eig(M10,'vector');
    [~, ind] = sort(eigvals);
    mesProj = eigvecs(:,ind(end));
    mesProj = mesProj*sign(mesProj(1));
    measurementParam(i) = 2*acos(mesProj(1)); % Take angle from z axis
%     measurementParam(i) = M10(1,1); % Just take the first element of matrix
end

figure
plot(v0./(v0+v1),measurementParam);

figure
hold on
for i = 1:numStateCoeffs
    plot(v0./(v0+v1),stateCoeffs(i,:));
end
hold off

%%
function plotClassicalStrategies(n,sym)
    hold on
    
    if n == 3
        v0 = 0:0.005:2;
        v1 = 2 - v0;
        ratio = v0./v1;
    
        % Classical
        qsw = (ratio <= 1).*(1/12*(2*v0 + 7*v1)) + (ratio > 1).*(1/12*(9*v0));
        plot(v0./(v0+v1), qsw);
        % Graph state
        plot(v0./(v0+v1), (v0+v1)/2);
    elseif n == 5           
        % Classical
        v0 = 0:0.005:2;
        v1 = 2 - v0;
        ratio = v0./v1;
        
        if ~sym
           qsw = (ratio <= 1/3).*(1/30*(8*v0 + 17*v1)) + (ratio > 1/3 & ratio <= 1).*(1/30*(6*v0 + 19*v1)) + (ratio > 1).*(1/30*(25*v0));
        else
           qsw = (ratio <= 1/3).*(1/30*(4*v0 + 11*v1)) + (ratio > 1/3 & ratio <= 1).*(1/30*(5*v0 + 20*v1)) + (ratio > 1).*(1/30*(25*v0));
        end
        plot(v0./(v0+v1), qsw);

        % Graph state
        if ~sym
            v0 = 2/3:0.005:2;
        else
            v0 = 1/2:0.005:2;
        end
        v1 = 2 - v0;
        plot(v0./(v0+v1), (v0+v1)/2);
    end
    hold off
end

%%
function plotNPABounds(n,sym)
    hold on
    
    loadNPAData;

    if n == 3
        plot(v0_C3/v0plusv1,QSW_NPA_C3);
    elseif n == 5           
        if ~sym
            plot(v0_C5_00/v0plusv1,QSW_NPA_C5_00);
        else
            plot(v0_C5_01/v0plusv1,QSW_NPA_C5_01);
        end
    end
    hold off
end
