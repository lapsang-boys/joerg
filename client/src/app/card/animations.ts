import { animation, style, animate, keyframes, state } from '@angular/animations';

export const fadeIn = animation([
	state('*', style({ opacity: 1})),
	state('void', style({ opacity: 0})),
	animate(
		'{{ time }}',
		keyframes([
			style({ opacity: '{{ from }}', offset: 0 }),
			style({ opacity: '{{ to }}', offset: 1 }),
		])
	)
]);
