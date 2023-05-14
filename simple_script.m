clear all;
close all;
clc;
N = 25;

% Average time required to finish the task
my_data_4 = [115.29 119.72 120.80 114.71 125.77 107.71 108.23 94.70 97.70 113.70 125.73 104.17 90.81 93.25 ...
    108.12 99.98 102.45 112.68 113.45 110.18 99.70 119.79 105.60 100.31 96.39];

my_data_5 = [149.26 161.87 147.32 151.90 134.28 126.25 150.26 135.74 176.69 167.06 180.88 133.82 153.93 141.06 ...
    137.90 147.90 138.68 141.06 159.51 151.82 147.93 143.45 140.89 157.98 160.18];

my_data_6 = [144.76 129.22 147.26 135.85 211.95 152.30 195.84 167.32 230.60 184.84 161.79 148.76 151.03 170.28 ...
    165.76 165.36 176.67 210.77 184.38 216.97 161.79 188.05 184.06 143.76 158.77];

ISA_data_4 = [49.74 55.86 51.56 54.91 48.72 51.14 53.64 50.45 53.46 41.72 41.73 48.16 47.00 50.43 55.07 51.86 46.77 ...
    44.58 50.54 50.51 47.25 48.12 40.25 52.17 50.60];

ISA_data_5 = [63.25 55.91 75.73 68.96 79.51 57.61 58.65 71.69 69.14 63.98 79.14 59.75 67.44 58.98 51.29 65.78 ...
    62.13 57.67 75.53 72.14 50.18 55.53 67.78 60.75 62.18];

ISA_data_6 = [85.25 73.38 79.28 73.41 102.91 106.34 80.35 109.61 98.97 109.55 84.62 109.04 111.12 90.18 102.36 70.27 ...
    84.16 91.27 90.56 100.74 70.25 78.77 87.78 82.45 71.35];

% Lilliefors test
h4_myData = lillietest(my_data_4);
h4_isaData = lillietest(ISA_data_4);
h5_myData = lillietest(my_data_5);
h5_isaData = lillietest(ISA_data_5);
h6_myData = lillietest(my_data_6);
h6_isaData = lillietest(ISA_data_6);


% T - test
h1 = ttest2(my_data_4,ISA_data_4,'Tail','right');
h2 = ttest2(my_data_5,ISA_data_5,'Tail','right');
h3 = ttest2(my_data_6,ISA_data_6,'Tail','right');

% AVG time
TestL = {'My algorithm'; 'Isabella algorithm'};
y = [mean(my_data_4) mean(ISA_data_4); mean(my_data_5) mean(ISA_data_5); mean(my_data_6) mean(ISA_data_6)];
figure(1)
b = bar(y);
ylim([0 180])
labels = {'4 tokens'; '5 tokens'; '6 tokens'};
set(gca,'xticklabel',labels)
title("AVG time comparison")
b(1).FaceColor = [0 0 1];
b(2).FaceColor = [1 0 0];
legend(TestL,'Location','northwest');


% Comparison of success/failures
TestL = {'Success','Failures'};
labels = {'My algorithm'; 'Isabella algorithm'};
y = [24 2; 24 1];
figure(2)
b = bar(y);
ylim([0 30])
set(gca,'xticklabel',labels)
title("Number of success and failures comparison for N = 4")
b(1).FaceColor = [0 1 0];
b(2).FaceColor = [1 0 0];
legend(TestL,'Location','northwest');

y = [22 3; 22 3];
figure(3)
b = bar(y);
ylim([0 30])
set(gca,'xticklabel',labels)
title("Number of success and failures comparison for N = 5")
b(1).FaceColor = [0 1 0];
b(2).FaceColor = [1 0 0];
legend(TestL,'Location','northwest');

labels = {'My algorithm'; 'Isabella algorithm'};
y = [20 5; 18 7];
figure(4)
b = bar(y);
ylim([0 30])
set(gca,'xticklabel',labels)
title("Number of success and failures comparison for N = 6")
b(1).FaceColor = [0 1 0];
b(2).FaceColor = [1 0 0];
legend(TestL,'Location','northwest');
