/**
 * Basic tests for Shadow Clone MCP Server
 */

import { test } from 'node:test';
import assert from 'node:assert';
import { CodingSensei } from '../lib/ninja.js';
import { ShadowCloneManager } from '../lib/shadowclone.js';
import { analyzeJutsu, getCloneCount, JutsuType } from '../lib/jutsu.js';

test('CodingSensei initialization', () => {
  const sensei = new CodingSensei('Test Sensei');
  assert.strictEqual(sensei.name, 'Test Sensei');
  assert.strictEqual(sensei.village, 'Coding Dojo');
  assert.strictEqual(sensei.rank, 'Sensei');
});

test('Jutsu analysis for different mission types', () => {
  assert.strictEqual(analyzeJutsu('Analyze this complex system'), JutsuType.MULTI_SHADOW_CLONE);
  assert.strictEqual(analyzeJutsu('Research the best practices'), JutsuType.CLONE_NETWORK);
  assert.strictEqual(analyzeJutsu('Fix this bug in the code'), JutsuType.DISPEL_CLONE);
  assert.strictEqual(analyzeJutsu('Convert this data format'), JutsuType.TRANSFORM_CLONE);
  assert.strictEqual(analyzeJutsu('Simple task execution'), JutsuType.SHADOW_CLONE);
});

test('Clone count calculation', () => {
  const shortMission = 'short';
  const longMission = 'a'.repeat(500);
  
  assert.ok(getCloneCount(JutsuType.SHADOW_CLONE, shortMission) >= 2);
  assert.ok(getCloneCount(JutsuType.MULTI_SHADOW_CLONE, longMission) >= 3);
  assert.strictEqual(getCloneCount(JutsuType.DISPEL_CLONE, 'any'), 1);
});

test('ShadowCloneManager basic functionality', async () => {
  const sensei = new CodingSensei('Test Sensei');
  const manager = new ShadowCloneManager(sensei);
  
  const status = manager.getStatus();
  assert.strictEqual(status.activeClones, 0);
  assert.strictEqual(status.completedMissions, 0);
});

test('Token efficiency simulation', async () => {
  const sensei = new CodingSensei('Test Sensei');
  const manager = new ShadowCloneManager(sensei);
  
  const result = await manager.createClones('Test mission for delegation', 1000);
  
  assert.ok(result.tokenStats.efficiency > 0);
  assert.ok(result.tokenStats.saved > 0);
  assert.ok(result.successfulClones > 0);
  assert.strictEqual(result.failedClones, 0);
});