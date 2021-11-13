%% KPERS benefit estimates (from 10/27/2021 summary)
colLabels = {'No Lump Sum' '10% Lump Sum' '20% Lump Sum' '30% Lump Sum' '40% Lump Sum' '50% Lump Sum'};
rowLabels = {'Maximum' '50% Joint-Survivor' '75% Joint-Survivor' '100% Joint-Survivor'...
             '5-Year Life-Certain' '10-Year Life-Certain' '15-Year Life-Certain'};
lumpSum = [0.00 64258.29 128516.57 192774.86 257033.14 321291.43];
monthlies = [5784.93 5206.44 4627.94 4049.45 3470.96 2892.47
             5403.13 4862.81 4322.50 3782.19 3241.88 2701.56
             5206.44 4685.79 4165.15 3644.51 3123.86 2603.22
             5009.75 4508.77 4007.80 3506.82 3005.85 2504.87
             5669.23 5102.31 4535.39 3968.46 3401.54 2834.62
             5495.68 4946.12 4396.55 3846.98 3297.41 2747.84
             5090.74 4581.66 4072.59 3563.52 3054.44 2545.37];

%% parameters
% dates
dateRetire = datenum('04/01/2022');
dateBirthC = datenum('05/17/1951');
dateBirthS = datenum('02/20/1957');
ageDiff = (dateBirthS - dateBirthC) / 365.25;

% life expectancies
ageLEC = 87.5;
ageLES = 83.9;
  % from https://www.ssa.gov/cgi-bin/longevity.cgi on 09/03/2021

% interest rate
APR = (1 + 0.07258) / (1 + 0.02733) - 1;  % inflation adjusted
  % 7.258% portfolio weighted returns as of 12/19/2020
  % 2.733% inflation is US average from 1981-2021
  % see https://kfknowledgebank.kaplan.co.uk/npv-with-inflation- for explanation:
  % * 7.258% is the money or nominal return for mutual fund investments
  % * 2.733% is the expected inflation
  % * (1 + nominal) = (1 + real) * (1 + inflation), therefore real = (1 + nominal) / (1 + inflation) - 1
  % * real rate is used as the discount rate since monthly payments don't have a COLA in the future and are therefore
  %   real (present dollar) quantities
  % see also https://xplaind.com/264707/npv-and-inflation
monRate = (1 + APR) ^ (1 / 12) - 1;

%% generate age axes and total retirement months
ageC = ((dateRetire - dateBirthC) / 365.25):(1 / 12):100;
ageS = ((dateRetire - dateBirthS) / 365.25):(1 / 12):100;

%% initialize NPV lookup vectors to accelerate later calculations
k1Powers = (1 ./ (1 + monRate) .^ (0 : (3 * max(length(ageC), length(ageS)) + 2)));
  % k1 = 1 / (1 + monRate)
  % k1Powers(1) has exponent 0, +2 on exponent range vector is to guarantee safe indexing below
k2 = 1 / (1 - k1Powers(2));
  % k2 = 1 / (1 - k)

%% allocate the calculation arrays and lookup vectors
values = zeros(length(ageS), length(ageC), numel(monthlies));
benefitRow = repmat(1:size(monthlies, 1), size(monthlies, 2), 1)(:);
benefitCol = repmat(1:size(monthlies, 2), 1, size(monthlies, 1))(:);
remMonS = repmat((0:(length(ageS) - 1)).', 1, length(ageC));
remMonC = repmat(0:(length(ageC) - 1), length(ageS), 1);
amountOne = zeros(length(ageS), length(ageC));

%% calculate the present values for all age-of-death pairs and benefit elections
for b = 1:numel(monthlies)  % benefit election
  % display status
  fprintf('benefit election %d/%d\n', b, numel(monthlies));

  % look up benefit table indices
  r = benefitRow(b);
  c = benefitCol(b);

  % determine NPV of monthly stream based on benefit election
  if (r == 1)  % maximum
    % monthly payments continue only while S is alive
    numMon = remMonS;
    monValue = monthlies(r, c) * ((k1Powers(1) - k1Powers(numMon + 2)) * k2 - 1);
      % -1 since starting at time 0 and there's no payment until the end of that period
  elseif (r >= 5) % life-certain
    % monthly payments continue the maximum of S's life or the guaranteed period, whichever is longer
    numMonGtd = 12 * 5 * (r - 4);  % r == 5 => 5 y, r == 6 => 10 y, r == 7 => 15 y
    numMon = max(numMonGtd, remMonS);
    monValue = monthlies(r, c) * ((k1Powers(1) - k1Powers(numMon + 2)) * k2 - 1);
      % -1 since starting at time 0 and there's no payment until the end of that period
  else  % joint-survivor
    % period where both C & S are alive
    numMonBoth = min(remMonS, remMonC);

    % period where only one of C & S are alive
    numMonOne = abs(remMonC - remMonS);
    amountOne(:, :) = monthlies(1, c);  % default to "maximum"
    proration = 1 + 0.25 * (r - 4);  % r == 2 => 0.5, r == 3 => 0.75, r == 4 => 1.0
    amountOne(remMonC < remMonS) = proration * monthlies(r, c);  % override with proration

    % combined timeline
    monValue = monthlies(r, c) .* ((k1Powers(1) - k1Powers(numMonBoth + 2)) * k2 - 1);
    monValue += amountOne .* (k1Powers(numMonBoth + 2) - k1Powers(numMonBoth + numMonOne + 2)) * k2;
      % no adjustment for period zero since resuming at the end of the previous series
  endif

  % combine the monthly NPV and lump sum components
  values(:, :, b) = lumpSum(c) + monValue;
endfor

%% plot NPVs
cMin = min(values(:));
cMax = max(values(:));
for b = 1:numel(monthlies)  % benefit election
  % look up benefit table indices
  r = benefitRow(b);
  c = benefitCol(b);

  % plot
  figure;
  imagesc(ageC, ageS, values(:, :, b) / 1e3);
  set(gca, 'ydir', 'normal', 'fontsize', 16);
  hold('on');
  plot([min(ageC) max(ageC)], [ageLES ageLES], ':w', 'linewidth', 2);
  plot([ageLEC ageLEC], [min(ageS) max(ageS)], ':w', 'linewidth', 2);
  plot([ageC(1) ageC(end)], [ageS(1) (ageC(end) - ageDiff)], 'w', 'linewidth', 2);
  axis('image');
  caxis([cMin cMax] ./ 1e3);
  xlabel('C age at death (y)');
  ylabel('S age at death (y)');
  title(sprintf('%d/%d: %s, %s', b, numel(monthlies), rowLabels{r}, colLabels{c}));
  h = colorbar;
  set(h, 'fontsize', 16);
  set(get(h, 'ylabel'), 'string', 'NPV ($k 2022)');
endfor

%% determine the best election for each age-of-death pairing
[bestNPV, bestElect] = max(values, [], 3);

%% plot best elections
% determine the number of unique elections and their labels
uniqueElects = unique(bestElect(:));
uniqueLabels = {};
for u = 1:length(uniqueElects)
  bestElect(bestElect == uniqueElects(u)) = -u;
  uniqueLabels{u} = sprintf('%s, %s', rowLabels{benefitRow(uniqueElects(u))},...
                                      colLabels{benefitCol(uniqueElects(u))});
endfor
bestElect *= -1;

% plot best elections
figure;
imagesc(ageC, ageS, bestElect);
set(gca, 'ydir', 'normal', 'fontsize', 16);
hold('on');
plot([min(ageC) max(ageC)], [ageLES ageLES], ':w', 'linewidth', 2);
plot([ageLEC ageLEC], [min(ageS) max(ageS)], ':w', 'linewidth', 2);
plot([ageC(1) ageC(end)], [ageS(1) (ageC(end) - ageDiff)], 'w', 'linewidth', 2);
axis('image');
xlabel('C age at death (y)');
ylabel('S age at death (y)');
title('best election by age pairs');
colormap(rainbow(length(uniqueElects)));
h = colorbar;
set(h, 'fontsize', 16, 'ytick', linspace(1.5, length(uniqueElects) - 0.5, length(uniqueElects)),...
       'yticklabel', uniqueLabels);

% plot NPVs with best elections
figure;
imagesc(ageC, ageS, bestNPV / 1e3);
set(gca, 'ydir', 'normal', 'fontsize', 16);
hold('on');
plot([min(ageC) max(ageC)], [ageLES ageLES], ':w', 'linewidth', 2);
plot([ageLEC ageLEC], [min(ageS) max(ageS)], ':w', 'linewidth', 2);
plot([ageC(1) ageC(end)], [ageS(1) (ageC(end) - ageDiff)], 'w', 'linewidth', 2);
axis('image');
xlabel('C age at death (y)');
ylabel('S age at death (y)');
title('best election NPV by age pairs');
h = colorbar;
set(h, 'fontsize', 16);
set(get(h, 'ylabel'), 'string', 'NPV ($k 2022)');

% plot foregone NPV by election
foregoneNPV = zeros(length(ageS), length(ageC), length(uniqueElects));
for u = 1:length(uniqueElects)
  foregoneNPV(:, :, u) = bestNPV - values(:, :, uniqueElects(u));
endfor
cMax = max(foregoneNPV(:)) / 1e3;
if (length(uniqueElects) <= 3)
  subCol = length(uniqueElects);
  subRow = 1;
else
  subCol = ceil(sqrt(length(uniqueElects)));
  subRow = ceil(length(uniqueElects) / subCol);
endif
figure;
for u = 1:length(uniqueElects)
  subplot(subRow, subCol, u);
  imagesc(ageC, ageS, foregoneNPV(:, :, u) / 1e3);
  caxis([0 cMax]);
  set(gca, 'ydir', 'normal', 'fontsize', 16);
  hold('on');
  plot([min(ageC) max(ageC)], [ageLES ageLES], ':w', 'linewidth', 2);
  plot([ageLEC ageLEC], [min(ageS) max(ageS)], ':w', 'linewidth', 2);
  plot([ageC(1) ageC(end)], [ageS(1) (ageC(end) - ageDiff)], 'w', 'linewidth', 2);
  axis('image');
  xlabel('C age at death (y)');
  ylabel('S age at death (y)');
  title(uniqueLabels{u});
  h = colorbar;
  set(h, 'fontsize', 16);
  set(get(h, 'ylabel'), 'string', 'foregone NPV ($k 2022)');
endfor
