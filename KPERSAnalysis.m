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

% life expectancies
ageLEC = 87.5;
ageLES = 83.9;
  % from https://www.ssa.gov/cgi-bin/longevity.cgi on 09/03/2021

% interest rate
APR = 0.07258;  % portfolio weighted returns as of 12/19/2020
monRate = (1 + APR) ^ (1 / 12) - 1;

%% generate age axes and total retirement months
ageC = ((dateRetire - dateBirthC) / 365.25):(1 / 12):100;
ageS = ((dateRetire - dateBirthS) / 365.25):(1 / 12):100;
numMonS = floor((dateBirthS + 365.25 * ageS - dateRetire) / (365.25 / 12));
numMonC = floor((dateBirthC + 365.25 * ageC - dateRetire) / (365.25 / 12));
  % average out leap years and days-per-month variations

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

  % loop through age-of-death pairings
  for v = 1:length(ageS)
    if (r == 1)  % maximum
      % monthly payments continue only while S is alive
      amounts = monthlies(r, c) * ones(numMonS(v), 1);
    elseif (r >= 5) % life-certain
      % monthly payments continue the maximum of S's life or the guaranteed period
      numMonGtd = 12 * 5 * (r - 4);  % r == 5 => 5 y, r == 6 => 10 y, r == 7 => 15 y
      numMon = max(numMonGtd, numMonS(v));
      amounts = monthlies(r, c) * ones(numMon, 1);
    endif
    monValue = npv(monRate, amounts, 0);

    for h = 1:length(ageC)
      if ((r >= 2) && (r <= 4))  % joint-survivor
        % period where both C & S are alive
        numMonBoth = min(numMonC(h), numMonS(v));
        amountBoth = monthlies(r, c);

        % period where only one of C & S are alive
        numMonOne = abs(numMonC(h) - numMonS(v));
        if (numMonS(v) < numMonC(h))  % C died after S
          proration = 1 + 0.25 * (r - 4);  % r == 2 => 0.5, r == 3 => 0.75, r == 4 => 1.0
          amountOne = proration * monthlies(r, c);
            % C's benefit is prorated based on benefit election
        else  % C died before S
          amountOne = monthlies(1, c);  % revert to "maximum" benefit election
        endif

        % combined timeline
        amounts = [amountBoth * ones(numMonBoth, 1); amountOne * ones(numMonOne, 1)];
        monValue = npv(monRate, amounts, 0);
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
  axis('image');
  caxis([cMin cMax] ./ 1e3);
  xlabel('C age at death (y)');
  ylabel('S age at death (y)');
  title(sprintf('%d/%d: %s, %s', b, numel(monthlies), rowLabels{r}, colLabels{c}));
  h = colorbar;
  set(h, 'fontsize', 16);
  set(get(h, 'ylabel'), 'string', 'NPV ($k 2021)');
endfor

%% determine the best election for each age-of-death pairing
best = zeros(length(ageS), length(ageC));
for v = 1:length(ageS)
  for h = 1:length(ageC)
    [~, best(v, h)] = max(values(v, h, :));
  endfor
endfor

%% plot best elections
% determine the number of unique elections and their labels
uniqueElections = unique(best(:));
uniqueLabels = {};
for u = 1:length(uniqueElections)
  best(best == uniqueElections(u)) = -u;
  uniqueLabels{u} = sprintf('%s, %s', rowLabels{benefitRow(uniqueElections(u))},...
                                      colLabels{benefitCol(uniqueElections(u))});
endfor
best *= -1;

% plot
figure;
imagesc(ageC, ageS, best);
set(gca, 'ydir', 'normal', 'fontsize', 16);
hold('on');
plot([min(ageC) max(ageC)], [ageLES ageLES], 'w', 'linewidth', 2);
plot([ageLEC ageLEC], [min(ageS) max(ageS)], 'w', 'linewidth', 2);
axis('image');
xlabel('C age at death (y)');
ylabel('S age at death (y)');
title('best election by age pairs');
colormap(rainbow(length(uniqueElections)));
h = colorbar;
set(h, 'fontsize', 16, 'ytick', linspace(1.5, length(uniqueElections) - 0.5, length(uniqueElections)),...
       'yticklabel', uniqueLabels);
