dataQuadrilJoeTor = importfile(filenameQuadrilJoeTor);

dataPelvePe = importfile(filenamePelvePe);

n_clicos_dir = n_clicos_dirControl;
n_ciclos_esq = n_clicos_esqControl;


%% Atenção aqui!!
% media_stance_dir = 62.3;
% std_stance_dir = 2.8;
% 
% media_stance_esq = 60.5;
% std_stance_esq = 3.5;


tempo=0:100;
%try

%Pelve Direita
%figure(1)
PelveD_Sag=dataPelvePe(:,3:3:n_clicos_dir*3+1);
% subplot(4,3,2)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,PelveD_Sag,'b-')
% title('Pelve - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-10 40])
% 
% plot([0 100],[0 0],'k-')
% yticks([-10 -5 0 15 30 40])
% yticklabels({'-10','-5','0','15','30','40'})
% t=text(-20,0,'Posterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Anterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})
% 

PelveD_Cor=dataPelvePe(:,2:3:n_clicos_dir*3+1)*-1;
% subplot(4,3,1)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,PelveD_Cor,'b-')
% title('Pelve - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 15])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -7.5 0 7.5 15])
% yticklabels({'-15','-7.5','0','7.5','15'})
% t=text(-20,-7.5,'Baixo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,7.5,'Cima','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


PelveD_Trans=dataPelvePe(:,4:3:n_clicos_dir*3+1);
% subplot(4,3,3)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,PelveD_Trans,'b-')
% title('Pelve - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-40 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-40 -20 0 20 40])
% yticklabels({'-40','-20','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


% Quadril Direito

QuadrilD_Sag=dataQuadrilJoeTor(:,2:3:n_clicos_dir*3+1);
% subplot(4,3,5)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,QuadrilD_Sag,'b-')
% title('Quadril - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 60])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -5 0 20 40 60])
% yticklabels({'-15','-5','0','20','40','60'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,50,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

QuadrilD_Cor=dataQuadrilJoeTor(:,3:3:n_clicos_dir*3+1);
% subplot(4,3,4)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,QuadrilD_Cor,'b-')
% title('Quadril - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 20])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 10 20])
% yticklabels({'-20','-10','0','10','20'})
% t=text(-20,-10,'Abdução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,10,'Adução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

QuadrilD_Trans=dataQuadrilJoeTor(:,4:3:n_clicos_dir*3+1);
% subplot(4,3,6)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,QuadrilD_Trans,'b-')
% title('Quadril - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 50])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 25 50])
% yticklabels({'-30','-15','0','25','50'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho Direito
JoelhoD_Sag=dataQuadrilJoeTor(:,((n_clicos_dir+1)*3-1)+3*n_ciclos_esq:3:(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir-1);
% subplot(4,3,8)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,80,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,JoelhoD_Sag,'b-')
% title('Joelho - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 80])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 20 40 80])
% yticklabels({'-20','-10','0','20','40','80'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,60,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

%% Joelho Direito
JoelhoD_Cor=dataQuadrilJoeTor(:,((n_clicos_dir+1)*3-1)+3*n_ciclos_esq+1:3:(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir-1);
% subplot(4,3,7)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,JoelhoD_Cor,'b-')
% title('Joelho - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Valgo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Varo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho Direito
JoelhoD_trans=dataQuadrilJoeTor(:,((n_clicos_dir+1)*3-1)+3*n_ciclos_esq+2:3:(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir-1);
% subplot(4,3,9)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,JoelhoD_trans,'b-')
% title('Joelho - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Tornozelo Direito
TornD_Sag=dataQuadrilJoeTor(:,((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq:3:(((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1)+3*n_clicos_dir);
% subplot(4,3,11)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,TornD_Sag,'b-')
% title('Tornozelo - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 45])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30 45])
% yticklabels({'-30','-15','0','15','30','45'})
% t=text(-20,-15,'Planti','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Dorsi','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})



TornD_Trans=dataPelvePe(:,(n_clicos_dir*3+2)+3*n_ciclos_esq+2:3:((n_clicos_dir*3+2)+3*n_ciclos_esq-1)+3*n_clicos_dir);
% subplot(4,3,12)
% hold on
% errorbar(repmat(media_stance_dir,1000,1),linspace(-60,60,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,TornD_Trans,'b-')
% title('Tornozelo - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-50 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-50 -25 0 20 40])
% yticklabels({'-50','-25','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})



% Pelve Esquerda

%figure(2)
PelveE_Sag=dataPelvePe(:,n_clicos_dir*3+3:3:(n_clicos_dir*3+2)+3*n_ciclos_esq-1);
% subplot(4,3,2)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,PelveE_Sag,'r-')
% title('Pelve - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-10 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-10 -5 0 15 30 40])
% yticklabels({'-10','-5','0','15','30','40'})
% t=text(-20,0,'Posterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Anterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


PelveE_Cor=dataPelvePe(:,n_clicos_dir*3+2:3:(n_clicos_dir*3+2)+3*n_ciclos_esq-1);
% subplot(4,3,1)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,PelveE_Cor,'r-')
% title('Pelve - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 15])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -7.5 0 7.5 15])
% yticklabels({'-15','-7.5','0','7.5','15'})
% t=text(-20,-7.5,'Baixo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,7.5,'Cima','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


PelveE_Trans=dataPelvePe(:,n_clicos_dir*3+4:3:(n_clicos_dir*3+2)+3*n_ciclos_esq-1)*-1;
% subplot(4,3,3)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,PelveE_Trans,'r-')
% title('Pelve - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-40 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-40 -20 0 20 40])
% yticklabels({'-40','-20','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})




% Quadril Esquerdo
QuadrilE_Sag=dataQuadrilJoeTor(:,(n_clicos_dir+1)*3-1:3:((n_clicos_dir+1)*3-1)+3*n_ciclos_esq-1);
% subplot(4,3,5)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,QuadrilE_Sag,'r-')
% title('Quadril - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 60])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -5 0 20 40 60])
% yticklabels({'-15','-5','0','20','40','60'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,50,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

QuadrilE_Cor=dataQuadrilJoeTor(:,(n_clicos_dir+1)*3:3:((n_clicos_dir+1)*3-1)+3*n_ciclos_esq-1);
% subplot(4,3,4)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,QuadrilE_Cor,'r-')
% title('Quadril - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 20])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 10 20])
% yticklabels({'-20','-10','0','10','20'})
% t=text(-20,-10,'Abdução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,10,'Adução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

QuadrilE_Trans=dataQuadrilJoeTor(:,(n_clicos_dir+1)*3+1:3:((n_clicos_dir+1)*3-1)+3*n_ciclos_esq-1);
% subplot(4,3,6)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,QuadrilE_Trans,'r-')
% title('Quadril - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 50])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 25 50])
% yticklabels({'-30','-15','0','25','50'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho esquerdo
JoelhoE_Sag=dataQuadrilJoeTor(:,(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir:3:((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1);
% subplot(4,3,8)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,80,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,JoelhoE_Sag,'r-')
% title('Joelho - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 80])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 20 40 80])
% yticklabels({'-20','-10','0','20','40','80'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,60,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

%% Joelho Esquerdo
JoelhoE_Cor=dataQuadrilJoeTor(:,(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir+1:3:((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1);
% subplot(4,3,7)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,JoelhoE_Cor,'r-')
% title('Joelho - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Valgo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Varo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho Esquerdo
JoelhoE_trans=dataQuadrilJoeTor(:,(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir+2:3:((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1);
% subplot(4,3,9)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,JoelhoE_trans,'r-')
% title('Joelho - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Tornozelo Esquerdo
TornE_Sag=dataQuadrilJoeTor(:,(((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1)+3*n_clicos_dir+1:3:((((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1)+3*n_clicos_dir)+3*n_ciclos_esq);
% subplot(4,3,11)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,TornE_Sag,'r-')
% title('Tornozelo - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 45])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30 45])
% yticklabels({'-30','-15','0','15','30','45'})
% t=text(-20,-15,'Planti','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Dorsi','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

TornE_Trans=dataPelvePe(:,((n_clicos_dir*3+2)+3*n_ciclos_esq-1)+3*n_clicos_dir+3:3:(((n_clicos_dir*3+2)+3*n_ciclos_esq-1)+3*n_clicos_dir)+3*n_ciclos_esq);
% subplot(4,3,12)
% hold on
% errorbar(repmat(media_stance_esq,1000,1),linspace(-60,60,1000),repmat(std_stance_esq,1000,1),'horizontal','color',[.75 .75 .75])
% plot([media_stance_esq media_stance_esq],[-80 80],'-k')
% plot(tempo,TornE_Trans,'r-')
% title('Tornozelo - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-50 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-50 -25 0 20 40])
% yticklabels({'-50','-25','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})
% 
% fig1 = figure(1);
% pos_fig1 = [0 0 720 1920];
% set(fig1,'Position',pos_fig1)
% 
% fig2 = figure(2);
% fig2.Position=[820 0 720 1920];
%  
%     

% catch    
%     
% %Pelve Direita
% figure(1)
PelveD_Sag=dataPelvePe(:,3:3:n_clicos_dir*3+1);
% subplot(4,3,2)
% hold on
%plot([media_stance_dir-std_stance_dir media_stance_dir+std_stance_dir],[mean([-10;40]) mean([-10;40])],'color',[.5 .5 .5],'LineWidth',85)
%errorbar(repmat(media_stance_dir,1000,1),linspace(-10,40,1000),repmat(std_stance_dir,1000,1),'horizontal','color',[.75 .75 .75])
%plot([media_stance_dir media_stance_dir],[-80 80],'-k')
% plot(tempo,PelveD_Sag,'b-')
% title('Pelve - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-10 40])
% 
% plot([0 100],[0 0],'k-')
% yticks([-10 -5 0 15 30 40])
% yticklabels({'-10','-5','0','15','30','40'})
% t=text(-20,0,'Posterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Anterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


PelveD_Cor=dataPelvePe(:,2:3:n_clicos_dir*3+1)*-1;
% subplot(4,3,1)
% plot(tempo,PelveD_Cor,'b-')
% title('Pelve - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 15])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -7.5 0 7.5 15])
% yticklabels({'-15','-7.5','0','7.5','15'})
% t=text(-20,-7.5,'Baixo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,7.5,'Cima','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})
% 

PelveD_Trans=dataPelvePe(:,4:3:n_clicos_dir*3+1);
% subplot(4,3,3)
% plot(tempo,PelveD_Trans,'b-')
% title('Pelve - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-40 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-40 -20 0 20 40])
% yticklabels({'-40','-20','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


% Quadril Direito

QuadrilD_Sag=dataQuadrilJoeTor(:,2:3:n_clicos_dir*3+1);
% subplot(4,3,5)
% plot(tempo,QuadrilD_Sag,'b-')
% title('Quadril - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 60])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -5 0 20 40 60])
% yticklabels({'-15','-5','0','20','40','60'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,50,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})
% 
QuadrilD_Cor=dataQuadrilJoeTor(:,3:3:n_clicos_dir*3+1);
% subplot(4,3,4)
% plot(tempo,QuadrilD_Cor,'b-')
% title('Quadril - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 20])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 10 20])
% yticklabels({'-20','-10','0','10','20'})
% t=text(-20,-10,'Abdução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,10,'Adução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

QuadrilD_Trans=dataQuadrilJoeTor(:,4:3:n_clicos_dir*3+1);
% subplot(4,3,6)
% plot(tempo,QuadrilD_Trans,'b-')
% title('Quadril - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 50])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 25 50])
% yticklabels({'-30','-15','0','25','50'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho Direito
JoelhoD_Sag=dataQuadrilJoeTor(:,((n_clicos_dir+1)*3-1)+3*n_ciclos_esq:3:(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir-1);
% subplot(4,3,8)
% plot(tempo,JoelhoD_Sag,'b-')
% title('Joelho - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 80])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 20 40 80])
% yticklabels({'-20','-10','0','20','40','80'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,60,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

%% Joelho Direito
JoelhoD_Cor=dataQuadrilJoeTor(:,((n_clicos_dir+1)*3-1)+3*n_ciclos_esq+1:3:(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir-1);
% subplot(4,3,7)
% plot(tempo,JoelhoD_Cor,'b-')
% title('Joelho - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Valgo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Varo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho Direito
JoelhoD_trans=dataQuadrilJoeTor(:,((n_clicos_dir+1)*3-1)+3*n_ciclos_esq+2:3:(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir-1);
% subplot(4,3,9)
% plot(tempo,JoelhoD_trans,'b-')
% title('Joelho - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Tornozelo Direito
TornD_Sag=dataQuadrilJoeTor(:,((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq:3:(((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1)+3*n_clicos_dir);
% subplot(4,3,11)
% plot(tempo,TornD_Sag,'b-')
% title('Tornozelo - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 45])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30 45])
% yticklabels({'-30','-15','0','15','30','45'})
% t=text(-20,-15,'Planti','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Dorsi','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})
% 


TornD_Trans=dataPelvePe(:,(n_clicos_dir*3+2)+3*n_ciclos_esq+2:3:((n_clicos_dir*3+2)+3*n_ciclos_esq-1)+3*n_clicos_dir);
% subplot(4,3,12)
% plot(tempo,TornD_Trans,'b-')
% title('Tornozelo - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-50 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-50 -25 0 20 40])
% yticklabels({'-50','-25','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})



% Pelve Esquerda

% figure(2)
PelveE_Sag=dataPelvePe(:,n_clicos_dir*3+3:3:(n_clicos_dir*3+2)+3*n_ciclos_esq-1);
% subplot(4,3,2)
% plot(tempo,PelveE_Sag,'r-')
% title('Pelve - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-10 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-10 -5 0 15 30 40])
% yticklabels({'-10','-5','0','15','30','40'})
% t=text(-20,0,'Posterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Anterior','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


PelveE_Cor=dataPelvePe(:,n_clicos_dir*3+2:3:(n_clicos_dir*3+2)+3*n_ciclos_esq-1);
% subplot(4,3,1)
% plot(tempo,PelveE_Cor,'r-')
% title('Pelve - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 15])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -7.5 0 7.5 15])
% yticklabels({'-15','-7.5','0','7.5','15'})
% t=text(-20,-7.5,'Baixo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,7.5,'Cima','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


PelveE_Trans=dataPelvePe(:,n_clicos_dir*3+4:3:(n_clicos_dir*3+2)+3*n_ciclos_esq-1)*-1;
% subplot(4,3,3)
% plot(tempo,PelveE_Trans,'r-')
% title('Pelve - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-40 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-40 -20 0 20 40])
% yticklabels({'-40','-20','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})
% 



% Quadril Esquerdo
QuadrilE_Sag=dataQuadrilJoeTor(:,(n_clicos_dir+1)*3-1:3:((n_clicos_dir+1)*3-1)+3*n_ciclos_esq-1);
% subplot(4,3,5)
% plot(tempo,QuadrilE_Sag,'r-')
% title('Quadril - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-15 60])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-15 -5 0 20 40 60])
% yticklabels({'-15','-5','0','20','40','60'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,50,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

QuadrilE_Cor=dataQuadrilJoeTor(:,(n_clicos_dir+1)*3:3:((n_clicos_dir+1)*3-1)+3*n_ciclos_esq-1);
% subplot(4,3,4)
% plot(tempo,QuadrilE_Cor,'r-')
% title('Quadril - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 20])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 10 20])
% yticklabels({'-20','-10','0','10','20'})
% t=text(-20,-10,'Abdução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,10,'Adução','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

QuadrilE_Trans=dataQuadrilJoeTor(:,(n_clicos_dir+1)*3+1:3:((n_clicos_dir+1)*3-1)+3*n_ciclos_esq-1);
% subplot(4,3,6)
% plot(tempo,QuadrilE_Trans,'r-')
% title('Quadril - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 50])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 25 50])
% yticklabels({'-30','-15','0','25','50'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho esquerdo
JoelhoE_Sag=dataQuadrilJoeTor(:,(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir:3:((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1);
% subplot(4,3,8)
% plot(tempo,JoelhoE_Sag,'r-')
% title('Joelho - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-20 80])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-20 -10 0 20 40 80])
% yticklabels({'-20','-10','0','20','40','80'})
% t=text(-20,-10,'Extensão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,60,'Flexão','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

%% Joelho Esquerdo
JoelhoE_Cor=dataQuadrilJoeTor(:,(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir+1:3:((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1);
% subplot(4,3,7)
% plot(tempo,JoelhoE_Cor,'r-')
% title('Joelho - Coronal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Valgo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Varo','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Joelho Esquerdo
JoelhoE_trans=dataQuadrilJoeTor(:,(((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir+2:3:((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1);
% subplot(4,3,9)
% plot(tempo,JoelhoE_trans,'r-')
% title('Joelho - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 30])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30])
% yticklabels({'-30','-15','0','15','30'})
% t=text(-20,-15,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,15,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})


%% Tornozelo Esquerdo
TornE_Sag=dataQuadrilJoeTor(:,(((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1)+3*n_clicos_dir+1:3:((((((n_clicos_dir+1)*3-1)+3*n_ciclos_esq)+3*n_clicos_dir)+3*n_ciclos_esq-1)+3*n_clicos_dir)+3*n_ciclos_esq);
% subplot(4,3,11)
% plot(tempo,TornE_Sag,'r-')
% title('Tornozelo - Sagital')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-30 45])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-30 -15 0 15 30 45])
% yticklabels({'-30','-15','0','15','30','45'})
% t=text(-20,-15,'Planti','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,30,'Dorsi','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

TornE_Trans=dataPelvePe(:,((n_clicos_dir*3+2)+3*n_ciclos_esq-1)+3*n_clicos_dir+3:3:(((n_clicos_dir*3+2)+3*n_ciclos_esq-1)+3*n_clicos_dir)+3*n_ciclos_esq);
% subplot(4,3,12)
% plot(tempo,TornE_Trans,'r-')
% title('Tornozelo - Transversal')
% xlabel('Ciclo (%)')
% xlim([0 100])
% ylim([-50 40])
% hold on
% plot([0 100],[0 0],'k-')
% yticks([-50 -25 0 20 40])
% yticklabels({'-50','-25','0','20','40'})
% t=text(-20,-20,'Externa','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% t=text(-20,20,'Interna','FontSize',8,'HorizontalAlignment','center');
% t.Rotation=90;
% ylabel({'Graus(º)';' '})

% fig1 = figure(1);
% pos_fig1 = [0 0 720 1920];
% set(fig1,'Position',pos_fig1)
% 
% fig2 = figure(2);
% fig2.Position=[820 0 720 1920];
% 
% end
% clear media_stance_dir
% clear media_stance_esq
% clear std_stance_dir
% clear std_stance_esq
% 
%daspect([1 1 1])