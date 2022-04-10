function [optQSW, optPWin, optRho, optPOVMs] = maxQswSeeSaw(game,d,initRho,initPOVMs,yalmipOptions)
%maxQswSeeSaw SeeSaw optimisation of QSW for game on cycle graphs

    tol = 1e-5;
    tolPWin = tol;
    tolQSW = 1e-4;
    tolPayout = 1e-6;
    
%     rho = initRho;
%     if isempty(initRho)
%         rho = RandomDensityMatrix(d^game.n);
%     end

    % M{k}(:,:,a_k,t_k)
    M = initPOVMs;
    
    MAX_ITERS_PWIN = 0;
    MAX_ITERS_QSW = 3;
    MAX_ITERS_PAYOUT = 50;
    
    optQSW = 0;
    optPWin = 0;
    optRho = RandomDensityMatrix(d^game.n);
    optPOVMs = {};
    
    %% First we optimise the winning probability
    i = 0;
    prevPWin = -1;
    pWin = zeros(1,game.n+1);
    while i < MAX_ITERS_PWIN && pWin(end) - prevPWin > tolPWin
        i = i + 1;
        prevPWin = pWin(end);
        
        [pWinRho, rho] = optPWinRho(game,d,M,yalmipOptions);
        pWin(1) = pWinRho;
        for k = 1:game.n
            [pWinM, M_k] = optPWinM(game,d,rho,M,k,yalmipOptions);
            pWin(k+1) = pWinM;
            % Update M with the new POVMs
            M{k} = M_k;
        end
        disp(['P_win after iteration ', num2str(i), ': ', num2str(pWin(end))]);
    end
    % Set the optimal best yet, in case we don't run following see-saws
    if i > 0
        optQSW = game.QSWFromStrategy(rho,M);
        optPWin = pWin(end);
        optRho = rho;
        optPOVMs = M;
    end
    
    %% Then the global QSW
    i = 0;
    prevQSW = -1;
    QSW = zeros(1,game.n+1);
    while i < MAX_ITERS_QSW && QSW(end) - prevQSW > tolQSW
        i = i + 1;
        prevQSW = QSW(end);
        
        [QSWRho, rho] = optQSWRho(game,d,M,yalmipOptions);
        QSW(1) = QSWRho;
        for k = 1:game.n
            [QSWM, M_k] = optQSWM(game,d,rho,M,k,yalmipOptions);
            QSW(k+1) = QSWM;
            % Update M with the new POVMs
            M{k} = M_k;
        end
        disp(['QSW after iteration ', num2str(i), ': ', num2str(QSW(end))]);
    end
    % Set the optimal best yet, in case we don't run following see-saw
    if i > 0
        optQSW = game.QSWFromStrategy(rho,M);
        optPWin = game.pWinFromQuantumStrategy(rho,M);
        optRho = rho;
        optPOVMs = M;
    end
    
    %% Then the payout of each player
    % We perform a see-saw that alternates between otpimising the QSW over the state,
    % and then a nested see-saw optimising the individual payout of the players
    i = 0;
    prevQSW = -1;
    QSW = 0; % we don't count "current" QSW since might not be an equilibrium
    foundEquilibrium = false;
    if MAX_ITERS_PAYOUT > 0 % Then we want to discout previous, possibly non equilibrium, QSWs
        optQSW = 0;
    end
    % Checking instead abs(QSW - prevQSW) > tolQSW could be more robust
    % but I've never seen cases where it goes down then up above the best yet
    while i < MAX_ITERS_PAYOUT && QSW - prevQSW > tolQSW
        i = i + 1;
        prevQSW = QSW;
        % We first optimise QSW on rho (get best state for current POVMs)
        % Starting by making it "nice" so symmetristaion actually helps
        if d == 2
            [rho, M] = PutStrategyInNiceBasis(rho,M);
        end
        [~, rho] = optQSWRho(game,d,M,yalmipOptions);
        % Now we want to iterate until no player is improving/changing their personal gain => equilibrium
        maxPlayerChange = Inf;
        payouts = zeros(1,game.n);
        prevPayouts = zeros(1,game.n);
        j = 0;
        while j < MAX_ITERS_PAYOUT && maxPlayerChange > tolPayout
            j = j + 1;

            % We first get the payout of each player with that state
            % We should do that before we update any POVMs to robustly ensure equilibrium
            for k = 1:game.n
                prevPayouts(k) = game.playerPayout(rho,M,k);
            end

            % Then we optimise the payout of each player
            for k = 1:game.n
                [payout_k, M_k] = optPayoutM(game,d,rho,M,k,yalmipOptions);
                payouts(k) = payout_k;
                % Update M with the new POVMs
                M{k} = M_k;
            end
            maxPlayerChange = max(abs(payouts - prevPayouts));
            QSW = game.QSWFromStrategy(rho,M);

            disp(['QSW and maxPlayerImprovement after iteration ', num2str(i), '.',num2str(j),...
                  ': (', num2str(QSW), ', ', num2str(maxPlayerChange), ')']);
        end
        % At this point either we didn't converge, or we have an equilibrium
        % We save current best state/POVM in case next step actually makes things worse!
        % (By optimising local payout, no guarantee we always increase QSW, so we might go "too far" by accident)
        if maxPlayerChange <= tolPayout && QSW > optQSW
            foundEquilibrium = true;
            optQSW = QSW;
            optPWin = game.pWinFromQuantumStrategy(rho,M);
            optRho = rho;
            optPOVMs = M;
        end
    end
    
    if ~foundEquilibrium && MAX_ITERS_PAYOUT > 0
       % We didn't converge, so we shouldn't record a misleading result. Set QSW to 0. 
       disp('Warning: did not to converge to equilibrium within tolerance.')
       optPWin = 0;
       optQSW = 0;
    end
    
    % Put things in a nicer basis
    if d == 2
        [optRho, optPOVMs] = PutStrategyInNiceBasis(optRho, optPOVMs);
    end

end

%%
function [optPWin, optRho] = optPWinRho(game,d,M,yalmipOptions)
%optPWinRho Optimise the state rho to give max PWin
    n = game.n;
    rho = sdpvar(d^n,d^n,'hermitian','real');
    constraints = [rho >= 0, trace(rho) == 1];

    pWin = game.pWinFromQuantumStrategy(rho,M);
    optimize(constraints, -pWin, yalmipOptions);
    
    optRho = value(rho);
    optPWin = value(pWin);
end

%%
function [optPWin, optM_k] = optPWinM(game,d,rho,M,k,yalmipOptions)
%optPWinM Optimise the measurements of party k to give max PWin
    M{k} = sdpvar(d,d,2,2,'hermitian','real');
    constraints = [M{k}(:,:,1,1) >= 0, M{k}(:,:,2,1) >= 0, M{k}(:,:,1,2) >= 0, M{k}(:,:,2,2) >= 0]; % PSD
    constraints = [constraints, M{k}(:,:,1,1) + M{k}(:,:,2,1) == eye(d), ...
                                M{k}(:,:,1,2) + M{k}(:,:,2,2) == eye(d)]; % Completeness
    
    pWin = game.pWinFromQuantumStrategy(rho,M);
    optimize(constraints, -pWin, yalmipOptions);
    
    optM_k = value(M{k});
    optPWin = value(pWin);
end

%%
function [optQSW, optRho] = optQSWRho(game,d,M,yalmipOptions)
%optQSWRho Optimise the state rho to give maximum QSW
    n = game.n;
    rho = sdpvar(d^n,d^n,'hermitian','real');
    constraints = [rho >= 0, trace(rho) == 1];
    % Ask the state to be (cyclicly) symmetric!
    constraints = [constraints, PermuteSystems(rho,[2:game.n 1],d*ones(1,game.n)) == rho];
    constraints = [constraints, PermuteSystems(rho,flip(1:game.n),d*ones(1,game.n)) == rho];

    QSW = game.QSWFromStrategy(rho,M);
    optimize(constraints, -QSW, yalmipOptions);
    
    optRho = value(rho);
    optQSW = value(QSW);
end

%%
function [optQSW, optM_k] = optQSWM(game,d,rho,M,k,yalmipOptions)
%optQSWM Optimise the measurements of party k to maximise overall QSW

    M{k} = sdpvar(d,d,2,2,'hermitian','real');
    constraints = [M{k}(:,:,1,1) >= 0, M{k}(:,:,2,1) >= 0, M{k}(:,:,1,2) >= 0, M{k}(:,:,2,2) >= 0]; % PSD
    constraints = [constraints, M{k}(:,:,1,1) + M{k}(:,:,2,1) == eye(d), ...
                                M{k}(:,:,1,2) + M{k}(:,:,2,2) == eye(d)]; % Completeness
    
    QSW = game.QSWFromStrategy(rho,M);
    optimize(constraints, -QSW, yalmipOptions);
    
    optM_k = value(M{k});
    optQSW = value(QSW);
end

%%
function [optPayoutK, optM_k] = optPayoutM(game,d,rho,M,k,yalmipOptions)
%optPayoutM Optimise the measurements of party k to maximise that party's payout

    M{k} = sdpvar(d,d,2,2,'hermitian','real');
    constraints = [M{k}(:,:,1,1) >= 0, M{k}(:,:,2,1) >= 0, M{k}(:,:,1,2) >= 0, M{k}(:,:,2,2) >= 0]; % PSD
    constraints = [constraints, M{k}(:,:,1,1) + M{k}(:,:,2,1) == eye(d), ...
                                M{k}(:,:,1,2) + M{k}(:,:,2,2) == eye(d)]; % Completeness
    
    payout_k = game.playerPayout(rho,M,k);
    optimize(constraints, -payout_k, yalmipOptions);
    
    optM_k = value(M{k});
    optPayoutK = value(payout_k);
end