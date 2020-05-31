export class Card {
	name: string;
	power: number;
	ruling: string;
	flavor: string;
	imgSrc: string;
	legendary: boolean;

	constructor(json: object) {
		this.name = json['name'];
		this.power = json['power'];
		this.ruling = json['ruling'];
		this.flavor = json['flavor'];
		this.imgSrc = json['imgSrc'];
		this.legendary = json['legendary'];
	}
}
