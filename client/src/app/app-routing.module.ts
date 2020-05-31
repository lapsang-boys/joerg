import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LibraryOverviewComponent } from './library/library-overview/library-overview.component';
import { HomeComponent } from './splashscreen/home/home.component';
import { GameLayoutComponent } from './game/layout/game-layout/game-layout.component';


const routes: Routes = [
	{
		path: '',
		component: HomeComponent
	},
	{
		path: 'library',
		component: LibraryOverviewComponent
	},
	{
		path: 'play',
		component: GameLayoutComponent
	},
	{ path: '**', redirectTo: '' }
];

@NgModule({
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule]
})
export class AppRoutingModule { }
