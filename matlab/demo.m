% P01 evaluation example; run this file from MATLAB.
% MATLAB execution has not been verified in the portfolio preparation environment.
here = fileparts(mfilename('fullpath'));
addpath(here);
filenameQuadrilJoeTor = fullfile(here,'..','examples','P01_001_QJT_E3D4.txt');
filenamePelvePe = fullfile(here,'..','examples','P01_001_PP_E3D4.txt');
n_clicos_dirControl = 4;
n_clicos_esqControl = 3;
run(fullfile(here,'processaMarchaControle.m'));
figure;
plot(tempo,JoelhoD_Sag,'b',tempo,JoelhoE_Sag,'r');
xlabel('Cycle (%)'); ylabel('Knee angle (degrees)');
title('P01 example');
