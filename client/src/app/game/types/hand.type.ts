import { Card } from "src/app/card/card.type";

export class Hand {
	cards: Card[];
	cardStates: Map<Card, HandCardState> = new Map();

	constructor(payload: object) {
		this.cards = (payload['hand'] as object[]).map(raw => new Card(raw));
		for (const [key, value] of Object.entries(payload['hand_states'])) {
			const matchingCard = this.cards.find((card => card.name == key));
			this.cardStates.set(matchingCard, HandCardState[value as keyof HandCardState]);
		}
	}
}

export enum HandCardState {
	VisibleOnlyForPlayer = 1,
	VisibleForEveryone = 2,
	HiddenFromEveryone = 3
}
