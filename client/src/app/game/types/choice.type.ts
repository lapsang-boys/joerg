import { FromJson } from 'src/app/network/from.json';

export class Choice implements FromJson {
	context: string;
	items: any[];
	numItems: number;

	fromJson(json: Object) {
		console.log("choice", json);
		this.context = json['context'];
		this.items = json['items'];
		this.numItems = json['numItems'];
	}
} 
