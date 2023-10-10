clear;
[my_input, fs ]= audioread('yemekhane_noisy_bogazici.wav');
[reference_noise, fs_noise ]= audioread('yemekhane_noise.wav');
reference=reference_noise(1:size(my_input));

order = 1000;
mu = 0.01;
window_size = ceil(25e-3*fs);
h = zeros(1,order);
input = my_input;
output = zeros(size(input));
total_window_number = floor(size(input,1)/window_size*2-1);
windowed_input = zeros(window_size,1);
windowed_output = zeros(window_size,1);
my_window=hamming(window_size);
shift=floor(window_size/2);

for i = 1:total_window_number
    delayed=zeros(1,order);
    windowed_input = my_window.*input(shift*(i-1)+1 : shift*(i-1)+window_size);
    my_reference = my_window.*reference(shift*(i-1)+1 : shift*(i-1)+window_size);
    for k = 1:window_size
        delayed(1) = my_reference(k);
        estimated_noise = delayed * h';
        windowed_output(k) = windowed_input(k) - estimated_noise ;
        h = h + 2*mu*(windowed_output(k) .* delayed);
        delayed(2:order)=delayed(1:order-1);     
    end
    output(shift*(i-1)+ 1 : shift*(i-1)+window_size) =output(shift*(i-1)+ 1 : shift*(i-1)+window_size) + windowed_output;
end
%% spectogram for this we look at SNR level 5dB and beta=5
s_input=spectrogram(input);
s_output=spectrogram(output);
figure();
spectrogram(input,'yaxis');
title('Noisy Signal');
figure();
spectrogram(output,'yaxis');
title('Enhanced Signal');
%% time plots of signals for this we look at SNR level 5dB and beta=5
figure();
subplot(2,1,1);
plot(input);
xlabel('Time');
ylabel('Noisy Signal');
title('Noisy Signal');
subplot(2,1,2);
plot(output);
xlabel('Time');
ylabel('Enhanced Signal');
title('Enhanced Signal');
