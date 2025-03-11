using Godot;
using System;
using System.Collections.Generic;

public partial class Stats : Node
{
	private Main _main;
	private Node _buildings;
	 Dictionary<string, int> myDictionary = new Dictionary<string, int>();

	public override void _Ready(){
		_main = GetParent<Main>();
		_buildings = _main.GetNode("Buildings");

		float totalSurfaceArea = CalcuateStats();
		GD.Print("Total Surface Area: ", totalSurfaceArea);
	}

	private float CalcuateStats(){
		float totalSurface = 0f;

		foreach (Node child in _buildings.GetChildren()){
			if (child is Building building){
				totalSurface += building.Surface;
			}
		}

		return totalSurface;
	}
}
