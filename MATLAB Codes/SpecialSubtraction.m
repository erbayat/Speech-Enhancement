clear;
[my_input, fs ]= audioread('Bogazici.wav');
snr_db = -20:1:20;
output_snr = zeros(size(snr_db));
window_size = ceil(25e-3*fs);
beta=10;
iteration=50;
shift=floor(window_size/2);
my_window=hamming(window_size);
figure;
plot(my_window);
xlabel('n');
title('Hamming Window');
ylabel('Amplitude');
set(gca, 'FontSize', 14);
xlim([0,1103]);
for k=1:iteration
    k
    for j = 1:length(snr_db)
        current_snr = snr_db(j);
        input = awgn(my_input,current_snr,'measured');
        output = zeros(length(input),1);
        reference = input(1:window_size);
        total_window_number = floor(size(input,1)/window_size*2-1);
        windowed_input = zeros(window_size,1);
        windowed_input_fft_abs = zeros(window_size,1);
        windowed_input_fft_phase = zeros(window_size,1);
        windowed_output = zeros(window_size,1);
        windowed_output_fft = zeros(window_size,1);
        reference_fft_abs = zeros(window_size,1);
        for i = 1:total_window_number
            windowed_input = my_window.*input(shift*(i-1)+1 : shift*(i-1)+window_size);
            windowed_input_fft_abs = fft(windowed_input);
            windowed_input_fft_phase = angle(windowed_input_fft_abs);
            windowed_input_fft_abs = abs(windowed_input_fft_abs); %Kafamiz karismasin
            reference_fft_abs = abs(fft(reference));
            dummy = windowed_input_fft_abs.^2 - beta*reference_fft_abs.^2;
            dummy(dummy<0) = 0;
            windowed_output_fft = (dummy).^(1/2).*exp(1j.*windowed_input_fft_phase);
            windowed_output = real(ifft(windowed_output_fft));
            Wn=2500/(fs/2);
            [B,A]=butter(4,Wn,'low');
            windowed_output=filter(B,A,windowed_output);
            output(shift*(i-1)+ 1 : shift*(i-1)+window_size) = output(shift*(i-1)+ 1 : shift*(i-1)+window_size)+windowed_output;
        end
        output_snr(j) = output_snr(j)+ snr(my_input, output - my_input);
        if (current_snr==5 && k==1)
            %% spectogram for this we look at SNR level 5dB and beta=5
            s_my_input=spectrogram(my_input);
            s_input=spectrogram(input);
            s_output=spectrogram(output);
            figure();
            spectrogram(my_input,'yaxis');
            title('Original Signal');
            figure();
            spectrogram(input,'yaxis');
            title('Noisy Signal');
            figure();
            spectrogram(output,'yaxis');
            title('Enhanced Signal');
            %% time plots of signals for this we look at SNR level 5dB and beta=5
            figure();
            subplot(3,1,1);
            plot(my_input);
            xlabel('Time');
            ylabel('Original Signal');
            title('Original Signal');
            subplot(3,1,2);
            plot(input);
            xlabel('Time');
            ylabel('Noisy Signal');
            title('Noisy Signal');
            subplot(3,1,3);
            plot(output);
            xlabel('Time');
            ylabel('Enhanced Signal');
            title('Enhanced Signal');
        end
    end
end
%%
output_snr=output_snr/iteration;

figure();
subplot(1,2,1);
plot(snr_db, output_snr,'-x');
xlabel('Input SNR (dB)');
ylabel('Output SNR (dB)');
%xlim([snr_db(1),snr_db(end)]);
title('Input SNR vs Output SNR');
grid on;
axis square;
set(gca, 'FontSize', 14);
subplot(1,2,2);
plot(snr_db, output_snr-snr_db,'-x');
xlabel('Input SNR (dB)');
ylabel('SNR Difference (dB)');
%xlim([snr_db(1),snr_db(end)]);
title('SNR Enchacement');
grid on;
axis square;
set(gca, 'FontSize', 14);
