% Loads the hierarchy result from data files

v0plusv1 = 2;

QSW_NPA_C3 = load('data/NPA_C3.txt')';
QSW_NPA_C5_00 = load('data/NPA_C5_00.txt')';
QSW_NPA_C5_01 = load('data/NPA_C5_01.txt')';

n_C3 = length(QSW_NPA_C3);
n_C5_00 = length(QSW_NPA_C5_00);
n_C5_01 = length(QSW_NPA_C5_01);

v0_C3 = 0:2/(n_C3-1):2;
v0_C5_00 = 0:2/(n_C5_00-1):2;
v0_C5_01 = 0:2/(n_C5_01-1):2;

v1_C3 = v0plusv1*ones(1,n_C3) - v0_C3;
v1_C5_00 = v0plusv1*ones(1,n_C5_00) - v0_C5_00;
v1_C5_01 = v0plusv1*ones(1,n_C5_01) - v0_C5_01;

ratio_C3 = v0_C3./v1_C3;
ratio_C5_00 = v0_C5_00./v1_C5_00;
ratio_C5_01 = v0_C5_01./v1_C5_01;

% %% Files for v0<v1, v0+v1=2 with v0 from 0 to 1
% QSW_NPA_C3_a = load('data/NPA_C3_a.txt')';
% QSW_NPA_C5_00_a = load('data/NPA_C5_00_a.txt')';
% QSW_NPA_C5_01_a = load('data/NPA_C5_01_a.txt')';
% 
% n_C3_a = length(QSW_NPA_C3_a);
% n_C5_00_a = length(QSW_NPA_C5_00_a);
% n_C5_01_a = length(QSW_NPA_C5_01_a);
% 
% v0_C3_a = 0:1/(n_C3_a-1):1;
% v0_C5_00_a = 0:1/(n_C5_00_a-1):1;
% v0_C5_01_a = 0:1/(n_C5_01_a-1):1;
% 
% v1_C3_a = v0plusv1*ones(1,n_C3_a) - v0_C3_a;
% v1_C5_00_a = v0plusv1*ones(1,n_C5_00_a) - v0_C5_00_a;
% v1_C5_01_a = v0plusv1*ones(1,n_C5_01_a) - v0_C5_01_a;
% 
% ratio_C3_a = v0_C3_a./v1_C3_a;
% ratio_C5_00_a = v0_C5_00_a./v1_C5_00_a;
% ratio_C5_01_a = v0_C5_01_a./v1_C5_01_a;
% 
% %% Files for v0>v1, v0+v1=2 with v0 from 1 to 2
% QSW_NPA_C3_b = load('data/NPA_C3_b.txt')';
% QSW_NPA_C5_00_b = load('data/NPA_C5_00_b.txt')';
% QSW_NPA_C5_01_b = load('data/NPA_C5_01_b.txt')';
% 
% n_C3_b = length(QSW_NPA_C3_b);
% n_C5_00_b = length(QSW_NPA_C5_00_b);
% n_C5_01_b = length(QSW_NPA_C5_01_b);
% 
% v0_C3_b = 1:1/(n_C3_b-1):2;
% v0_C5_00_b = 1:1/(n_C5_00_b-1):2;
% v0_C5_01_b = 1:1/(n_C5_01_b-1):2;
% 
% v1_C3_b = v0plusv1*ones(1,n_C3_b) - v0_C3_b;
% v1_C5_00_b = v0plusv1*ones(1,n_C5_00_b) - v0_C5_00_b;
% v1_C5_01_b = v0plusv1*ones(1,n_C5_01_b) - v0_C5_01_b;
% 
% ratio_C3_b = v0_C3_b./v1_C3_b;
% ratio_C5_00_b = v0_C5_00_b./v1_C5_00_b;
% ratio_C5_01_b = v0_C5_01_b./v1_C5_01_b;
% 
% %% Combined data: stick the lists together, removing the duplicate middle element
% 
% QSW_NPA_C3 = [QSW_NPA_C3_a, QSW_NPA_C3_b(2:end)];
% QSW_NPA_C5_00 = [QSW_NPA_C5_00_a, QSW_NPA_C5_00_b(2:end)];
% QSW_NPA_C5_01 = [QSW_NPA_C5_01_a, QSW_NPA_C5_01_b(2:end)];
% 
% n_C3 = length(QSW_NPA_C3);
% n_C5_00 = length(QSW_NPA_C5_00);
% n_C5_01 = length(QSW_NPA_C5_01);
% 
% v0_C3 = [v0_C3_a, v0_C3_b(2:end)];
% v0_C5_00 = [v0_C5_00_a, v0_C5_00_b(2:end)];
% v0_C5_01 = [v0_C5_01_a, v0_C5_01_b(2:end)];
% 
% v1_C3 = v0plusv1*ones(1,n_C3) - v0_C3;
% v1_C5_00 = v0plusv1*ones(1,n_C5_00) - v0_C5_00;
% v1_C5_01 = v0plusv1*ones(1,n_C5_01) - v0_C5_01;
% 
% ratio_C3 = v0_C3./v1_C3;
% ratio_C5_00 = v0_C5_00./v1_C5_00;
% ratio_C5_01 = v0_C5_01./v1_C5_01;