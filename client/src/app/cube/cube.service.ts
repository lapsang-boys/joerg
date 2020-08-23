import { Injectable } from '@angular/core';
import { Cube } from './cube.type';
import { Card } from '../card/card.type';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CubeService {
  private cubeSubject: Subject<Cube> = new Subject();
  private _cube: Cube = new Cube("Weasel Madness");

  constructor() { }
  get cube(): Observable<Cube> {
	return this.cubeSubject.asObservable();
  }

  add(card: Card): void {
	this._cube.cards.push(card);
	this.update();
  }

  update(cube?: Cube): void {
    if (cube) {
      this._cube = cube;
    }
    this.cubeSubject.next(this._cube);
  }
}
