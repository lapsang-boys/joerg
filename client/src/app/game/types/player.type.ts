import { Hand } from './hand.type';

export class Player {
	name: string;
	id: number;
	index: number;
	hand: Hand;

	constructor(payload: object) {
		this.index = payload['num'];
		this.name = payload['Name'];
		this.id = this.index;
		this.hand = new Hand(payload);
	}
}
