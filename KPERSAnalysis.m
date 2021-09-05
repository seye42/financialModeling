%% KPERS benefit estimates (from 08/26/2019 summary)
colLabels = {'No Lump Sum' '10% Lump Sum' '20% Lump Sum' '30% Lump Sum' '40% Lump Sum' '50% Lump Sum'};
rowLabels = {'Maximum' '50% Joint-Survivor' '75% Joint-Survivor' '100% Joint-Survivor'...
             '5-Year Life-Certain' '10-Year Life-Certain' '15-Year Life-Certain'};
lumpSum = [0.00 64168.49 128336.97 192505.46 256673.94 320842.43];
monthlies = [5776.85 5199.16 4621.48 4043.79 3466.11 2888.42
             5395.57 4856.02 4316.46 3776.90 3237.34 2697.79
             5199.16 4679.25 4159.33 3639.41 3119.50 2599.58
             5002.75 4502.47 4002.20 3501.92 3001.65 2501.37
             5661.31 5095.18 4529.05 3962.92 3396.79 2830.65
             5488.00 4939.20 4390.40 3841.60 3292.80 2744.00
             5083.62 4575.26 4066.90 3558.54 3050.17 2541.81];

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
APR = 0.07258;  % portfolio weighted returns as of 12/19/2020
monRate = (1 + APR) ^ (1 / 12) - 1;

%% generate age axes and total retirement months
ageC = ((dateRetire - dateBirthC) / 365.25):(3 / 12):100;
ageS = ((dateRetire - dateBirthS) / 365.25):(3 / 12):100;

%% initialize NPV lookup vectors to accelerate later calculations
k1Powers = (1 ./ (1 + monRate) .^ (0 : (3 * max(length(ageC), length(ageS)) + 2)));
  % k1 = 1 / (1 + monRate)
  % k1Powers(1) has exponent 0, +2 on exponent range vector is to guarantee safe indexing below
k2 = 1 / (1 - k1Powers(2));
  % k2 = 1 / (1 - k)

%% allocate the values cube and benefit election lookup vectors
values = zeros(length(ageS), length(ageC), numel(monthlies));
benefitRow = repmat(1:size(monthlies, 1), size(monthlies, 2), 1)(:);
benefitCol = repmat(1:size(monthlies, 2), 1, size(monthlies, 1))(:);

%% calculate the present values for all age-of-death pairs and benefit elections
for b = 1:numel(monthlies)  % benefit election
  % display status
  fprintf('benefit election %d/%d\n', b, numel(monthlies));

  % look up benefit table indices
  r = benefitRow(b);
  c = benefitCol(b);

  % hoist loop invariants 
  amountBoth = monthlies(r, c);
  proration = 1 + 0.25 * (r - 4);  % r == 2 => 0.5, r == 3 => 0.75, r == 4 => 1.0
  amountProrated = proration * amountBoth;
  amountMaximum = monthlies(1, c);  
  numMonGtd = 12 * 5 * (r - 4);  % r == 5 => 5 y, r == 6 => 10 y, r == 7 => 15 y

  % loop through age-of-death pairings
  for v = 1:length(ageS)
    if (r == 1)  % maximum
      % monthly payments continue only while S is alive
      numMon = 3 * v - 1;
    elseif (r >= 5) % life-certain
      % monthly payments continue the maximum of S's life or the guaranteed period, whichever is longer
      numMon = max(numMonGtd, 3 * v - 1);
    endif
    monValue = monthlies(r, c) * ((k1Powers(1) - k1Powers(numMon + 2)) * k2 - 1);
      % -1 since starting at time 0 and there's no payment until the end of that period

    for h = 1:length(ageC)
      if ((r >= 2) && (r <= 4))  % joint-survivor
        % period where both C & S are alive
        numMonBoth = min(3 * h - 1, 3 * v - 1);

        % period where only one of C & S are alive
        numMonOne = abs(3 * h - 3 * v);
        if (v < h)  % C died after S
          amountOne = amountProrated;
            % C's benefit is prorated based on benefit election
        else  % C died before S
          amountOne = amountMaximum;  % revert to "maximum" benefit election
        endif

        % combined timeline
        monValue = amountBoth * ((k1Powers(1) - k1Powers(numMonBoth + 2)) * k2 - 1);
        monValue += amountOne * (k1Powers(numMonBoth + 2) - k1Powers(numMonBoth + numMonOne + 2)) * k2;
          % no adjustment for period zero since resuming at the end of the previous series
      endif
        % all other cases for r are handled above this loop

      % calculate total net present value
      values(v, h, b) = lumpSum(c) + monValue;
    endfor
  endfor
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
bestNPV   = zeros(length(ageS), length(ageC));
bestElect = zeros(length(ageS), length(ageC));
for v = 1:length(ageS)
  for h = 1:length(ageC)
    [bestNPV(v, h), bestElect(v, h)] = max(values(v, h, :));
  endfor
endfor

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
