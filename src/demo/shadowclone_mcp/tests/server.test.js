#!/usr/bin/env node

/**
 * Tests for Shadow Clone MCP Server
 * 
 * Uses Node.js built-in test runner (node --test)
 */

import { test, describe } from 'node:test';
import assert from 'node:assert';
import { MainNinja } from '../lib/ninja.js';
import { ShadowCloneManager } from '../lib/shadowclone.js';
import { analyzeJutsu, getCloneCount, calculateTokenAllocation, JutsuType } from '../lib/jutsu.js';

describe('Jutsu Analysis', () => {
  test('should identify multi shadow clone jutsu for analysis tasks', () => {
    const mission = 'Analyze the complex system architecture and design optimization strategy';
    const jutsu = analyzeJutsu(mission);
    assert.strictEqual(jutsu, JutsuType.MULTI_SHADOW_CLONE);
  });

  test('should identify clone network jutsu for research tasks', () => {
    const mission = 'Research market trends and gather competitive intelligence';
    const jutsu = analyzeJutsu(mission);
    assert.strictEqual(jutsu, JutsuType.CLONE_NETWORK);
  });

  test('should identify transform clone jutsu for conversion tasks', () => {
    const mission = 'Convert XML data to JSON format with validation';
    const jutsu = analyzeJutsu(mission);
    assert.strictEqual(jutsu, JutsuType.TRANSFORM_CLONE);
  });

  test('should identify dispel clone jutsu for debugging tasks', () => {
    const mission = 'Fix memory leak and debug authentication errors';
    const jutsu = analyzeJutsu(mission);
    assert.strictEqual(jutsu, JutsuType.DISPEL_CLONE);
  });

  test('should default to shadow clone for general tasks', () => {
    const mission = 'Complete the project deliverables';
    const jutsu = analyzeJutsu(mission);
    assert.strictEqual(jutsu, JutsuType.SHADOW_CLONE);
  });
});

describe('Clone Count Calculation', () => {
  test('should calculate appropriate clone count for multi shadow clone', () => {
    const mission = 'A'.repeat(500); // Long mission
    const count = getCloneCount(JutsuType.MULTI_SHADOW_CLONE, mission);
    assert(count >= 3 && count <= 8, `Clone count ${count} should be between 3 and 8`);
  });

  test('should limit clone count to maximum', () => {
    const mission = 'A'.repeat(2000); // Very long mission
    const count = getCloneCount(JutsuType.MULTI_SHADOW_CLONE, mission);
    assert(count <= 8, `Clone count ${count} should not exceed 8`);
  });

  test('should ensure minimum clone count', () => {
    const mission = 'Short'; // Very short mission
    const count = getCloneCount(JutsuType.MULTI_SHADOW_CLONE, mission);
    assert(count >= 3, `Clone count ${count} should be at least 3 for multi shadow clone`);
  });
});

describe('Token Allocation', () => {
  test('should calculate correct token allocation', () => {
    const totalTokens = 1000;
    const jutsuType = JutsuType.SHADOW_CLONE; // 65% efficiency
    const cloneCount = 4;
    
    const allocation = calculateTokenAllocation(totalTokens, jutsuType, cloneCount);
    const expected = Math.floor((1000 * 0.35) / 4); // 87 tokens per clone
    
    assert.strictEqual(allocation, expected);
  });

  test('should handle zero clones gracefully', () => {
    const allocation = calculateTokenAllocation(1000, JutsuType.SHADOW_CLONE, 0);
    assert.strictEqual(allocation, 1000); // Should allocate all tokens when no clones
  });

  test('should allocate more tokens for less efficient jutsu', () => {
    const totalTokens = 1000;
    const multiCloneAllocation = calculateTokenAllocation(totalTokens, JutsuType.MULTI_SHADOW_CLONE, 4);
    const dispelAllocation = calculateTokenAllocation(totalTokens, JutsuType.DISPEL_CLONE, 4);
    
    assert(dispelAllocation > multiCloneAllocation, 'Dispel clone should get more tokens per clone');
  });
});

describe('Shadow Clone Manager', () => {
  test('should create and manage clones correctly', async () => {
    const ninja = new MainNinja('Test Ninja');
    const manager = new ShadowCloneManager(ninja);
    
    const result = await manager.createClones('Test mission for clone management', 800);
    
    assert(result.missionId, 'Should generate mission ID');
    assert.strictEqual(result.originalMission, 'Test mission for clone management');
    assert(result.cloneCount > 0, 'Should create at least one clone');
    assert(result.tokenStats, 'Should include token statistics');
    assert(result.tokenStats.efficiency > 0, 'Should show positive efficiency');
  });

  test('should track successful and failed clones', async () => {
    const ninja = new MainNinja('Test Ninja');
    const manager = new ShadowCloneManager(ninja);
    
    const result = await manager.createClones('Simple test mission', 500);
    
    assert(typeof result.successfulClones === 'number', 'Should track successful clones');
    assert(typeof result.failedClones === 'number', 'Should track failed clones');
    assert.strictEqual(result.successfulClones + result.failedClones, result.cloneCount);
  });

  test('should calculate token savings correctly', async () => {
    const ninja = new MainNinja('Test Ninja');
    const manager = new ShadowCloneManager(ninja);
    
    const maxTokens = 1000;
    const result = await manager.createClones('Token efficiency test mission', maxTokens);
    
    assert(result.tokenStats.allocated === maxTokens, 'Should track allocated tokens');
    assert(result.tokenStats.used < maxTokens, 'Should use fewer tokens than allocated');
    assert(result.tokenStats.saved > 0, 'Should save tokens');
    assert(result.tokenStats.efficiency > 0, 'Should show efficiency percentage');
  });
});

describe('Main Ninja', () => {
  test('should initialize with correct defaults', () => {
    const ninja = new MainNinja();
    
    assert.strictEqual(ninja.name, 'Naruto');
    assert.strictEqual(ninja.village, 'Hidden Leaf');
    assert.strictEqual(ninja.rank, 'Genin');
    assert.strictEqual(ninja.chakra, 1000);
    assert.strictEqual(ninja.stats.missionsCompleted, 0);
  });

  test('should execute missions and update stats', async () => {
    const ninja = new MainNinja('Test Ninja');
    
    const result = await ninja.executeMission('Test mission execution', { maxTokens: 500 });
    
    assert(result.ninja, 'Should return ninja info');
    assert(result.mission, 'Should return mission info');
    assert(result.summary, 'Should return mission summary');
    assert.strictEqual(ninja.stats.missionsCompleted, 1, 'Should increment mission counter');
  });

  test('should promote ninja based on performance', async () => {
    const ninja = new MainNinja('Promotion Test');
    
    // Complete 5 missions to trigger promotion
    for (let i = 0; i < 5; i++) {
      await ninja.executeMission(`Mission ${i + 1}`, { maxTokens: 500 });
    }
    
    // Should be promoted from Genin to Chunin if efficiency is good
    if (ninja.stats.averageEfficiency >= 60) {
      assert.strictEqual(ninja.rank, 'Chunin', 'Should be promoted to Chunin');
    }
  });

  test('should maintain mission history', async () => {
    const ninja = new MainNinja('History Test');
    
    await ninja.executeMission('First mission', { maxTokens: 300 });
    await ninja.executeMission('Second mission', { maxTokens: 400 });
    
    const history = ninja.getMissionHistory(2);
    assert.strictEqual(history.length, 2, 'Should maintain mission history');
    assert.strictEqual(history[0].mission, 'Second mission', 'Should return most recent first');
    assert.strictEqual(history[1].mission, 'First mission', 'Should maintain chronological order');
  });

  test('should handle status queries correctly', () => {
    const ninja = new MainNinja('Status Test');
    const status = ninja.getStatus();
    
    assert(status.ninja, 'Should include ninja info');
    assert(status.cloneManager, 'Should include clone manager status');
    assert(status.recentMissions, 'Should include recent missions');
    assert(Array.isArray(status.recentMissions), 'Recent missions should be array');
  });
});

describe('Integration Tests', () => {
  test('should demonstrate end-to-end mission execution', async () => {
    const ninja = new MainNinja('Integration Test Ninja');
    
    const missions = [
      'Analyze complex system architecture',
      'Research new technologies and frameworks',
      'Convert data format from XML to JSON',
      'Fix bugs and cleanup legacy code'
    ];
    
    let totalEfficiency = 0;
    
    for (const mission of missions) {
      const result = await ninja.executeMission(mission, { maxTokens: 800 });
      totalEfficiency += result.mission.result.tokenStats.efficiency;
      
      assert(result.mission.result.tokenStats.efficiency > 0, 'Each mission should be efficient');
    }
    
    const avgEfficiency = totalEfficiency / missions.length;
    assert(avgEfficiency > 50, `Average efficiency ${avgEfficiency}% should be over 50%`);
    assert.strictEqual(ninja.stats.missionsCompleted, missions.length, 'Should complete all missions');
  });

  test('should handle concurrent mission execution', async () => {
    const ninja = new MainNinja('Concurrent Test Ninja');
    
    const missions = [
      'Concurrent mission 1',
      'Concurrent mission 2',
      'Concurrent mission 3'
    ];
    
    // Execute missions concurrently
    const results = await Promise.all(
      missions.map(mission => ninja.executeMission(mission, { maxTokens: 500 }))
    );
    
    assert.strictEqual(results.length, 3, 'Should handle concurrent missions');
    assert.strictEqual(ninja.stats.missionsCompleted, 3, 'Should track all missions');
    
    // All missions should have completed successfully
    results.forEach(result => {
      assert(result.mission.result.tokenStats.efficiency > 0, 'Each concurrent mission should be efficient');
    });
  });
});

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('🧪 Running Shadow Clone MCP Server Tests...\n');
}