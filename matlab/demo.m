% Synthetic demonstration; run this file from MATLAB.
% MATLAB execution has not been verified in the portfolio preparation environment.
here = fileparts(mfilename('fullpath'));
addpath(here);
filenameQuadrilJoeTor = fullfile(here,'..','examples','synthetic_evaluation_QJT.txt');
filenamePelvePe = fullfile(here,'..','examples','synthetic_evaluation_PP.txt');
n_clicos_dirControl = 2;
n_clicos_esqControl = 3;
run(fullfile(here,'processaMarchaControle.m'));
figure;
plot(tempo,JoelhoD_Sag,'b',tempo,JoelhoE_Sag,'r');
xlabel('Cycle (%)'); ylabel('Knee angle (degrees)');
title('Synthetic demonstration');
